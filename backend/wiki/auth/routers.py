import logging

from fastapi import APIRouter, Request, Response, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from wiki.auth.authenticators.verification_code import VerificationCodeAuthenticatorInterface
from wiki.auth.authenticators.wiki_token import WikiTokenAuthenticatorInterface
from wiki.auth.deps import get_user
from wiki.auth.resolvers.email import EmailResolver
from wiki.auth.schemas import (
    UserLogin,
    UserSignResponse,
    VerifyTokenData,
    UserVerifyResponse,
    AccessTokenData,
    VerifyData,
    UserHandlerData,
    UserSignupSchema,
    VerificationType
)
from wiki.common.exceptions import WikiException, WikiErrorCode
from wiki.config import settings
from wiki.database.deps import get_db
from wiki.user.repository import UserRepository
from wiki.wiki_email.core import EmailProvider
from wiki.wiki_email.deps import get_email_provider
from wiki.wiki_email.schemas import EmailSchema

auth_router = APIRouter()
wiki_logger = logging.getLogger(__name__)


@auth_router.post(
    "/login",
    response_model=UserSignResponse,
    status_code=status.HTTP_202_ACCEPTED,
    description="The endpoint for sending an email and receiving a login confirmation token."
                "A confirmation code will be sent to the specified email."
)
async def login(user_in: UserLogin,
                request: Request,
                session: AsyncSession = Depends(get_db),
                email_provider: EmailProvider = Depends(get_email_provider)):
    authenticator = VerificationCodeAuthenticatorInterface(session)
    code = authenticator.verification_code
    token = await authenticator.create_verify_token(VerifyTokenData(
        email=user_in.email,
        user_ip=request.client.host,
        user_agent=request.headers.get("User-Agent")),
        verification_code=code
    )

    await email_provider.send_mail(EmailSchema(
        email=[user_in.email],
        code=code,
        subject="Your verification code to log in to the Wiki."
    ))
    wiki_logger.info(f"{user_in.email}: {code}")

    return UserSignResponse(email_to=user_in.email, verify_token=token)


@auth_router.post(
    "/signup",
    response_model=UserSignResponse,
    status_code=status.HTTP_202_ACCEPTED,
    description="Sending an application for registration in the system"
)
async def signup(user_signup: UserSignupSchema,
                 request: Request,
                 session: AsyncSession = Depends(get_db),
                 email_provider: EmailProvider = Depends(get_email_provider)):
    user_repository: UserRepository = UserRepository(session)
    is_available: bool = await user_repository.check_user_identification_data_is_available(user_signup.email)
    if not is_available:
        raise WikiException(
            message="Your username or email is not available or you have already sent an application.",
            error_code=WikiErrorCode.USER_NOT_SPECIFIED,
            http_status_code=status.HTTP_409_CONFLICT
        )
    if not user_signup.is_user_agreement_accepted:
        raise WikiException(
            message="You must accept the user agreement.",
            error_code=WikiErrorCode.USER_NOT_SPECIFIED,
            http_status_code=status.HTTP_400_BAD_REQUEST
        )
    email_resolver = EmailResolver(session)
    await email_resolver.resolve(user_signup.email)

    authenticator = VerificationCodeAuthenticatorInterface(session)
    code = authenticator.verification_code
    verify_token = VerificationCodeAuthenticatorInterface.create_verify_token(VerifyTokenData(
        email=user_signup.email,
        user_ip=request.client.host,
        user_agent=request.headers.get("User-Agent"),
        appointment=VerificationType.signup
    ), code)

    # Form an application and create a user

    # await email_provider.send_mail(EmailSchema(
    #     email=[user_signup.email],
    #     code=code,
    #     subject="Your verification code to confirm your signup."
    # ))
    wiki_logger.info(f"{user_signup.email}: {code}")

    return UserSignResponse(
        email_to=user_signup.email,
        verify_token=verify_token
    )


@auth_router.get(
    "/verify",
    response_model=UserVerifyResponse,
    status_code=status.HTTP_200_OK,
    description="Endpoint for confirming the code received by mail, issuing access token to perform authorized actions."
)
async def verify(response: Response,
                 data: VerifyData = Depends(),
                 session: AsyncSession = Depends(get_db)):
    authenticator = VerificationCodeAuthenticatorInterface(session, verification_code=data.code)
    data = await authenticator.validate(data.token)
    if isinstance(data, UserHandlerData):
        token = WikiTokenAuthenticatorInterface.create_access_token(AccessTokenData(
            email=data["email"],
            api_client_id=data["wiki_api_client"].id
        ))
        response.set_cookie(settings.AUTH_ACCESS_TOKEN_COOKIE_NAME,
                            token,
                            settings.AUTH_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
                            settings.AUTH_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
                            settings.AUTH_TOKEN_COOKIE_PATH,
                            settings.AUTH_TOKEN_COOKIE_DOMAIN,
                            settings.AUTH_TOKEN_COOKIE_SECURE,
                            settings.AUTH_TOKEN_COOKIE_HTTP_ONLY,
                            settings.AUTH_TOKEN_COOKIE_SAME_SITE)
    else:
        # Confirm application
        pass


@auth_router.post(
    "/test",
    status_code=status.HTTP_200_OK,
    description="Test endpoint to test the access token."
)
async def test(user: UserHandlerData = Depends(get_user)):
    return f"You have accessed a secure endpoint.. Your email: {user['email']}"
