import logging

from fastapi import APIRouter, Request, Response, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from wiki.auth.authenticators.verification_code import VerificationCodeAuthenticatorInterface
from wiki.auth.authenticators.wiki_token import WikiTokenAuthenticatorInterface
from wiki.auth.schemas import (
    FrontendUserLogin,
    UserSignResponse,
    VerifyTokenData,
    AccessTokenData,
    VerifyData,
    VerificationType
)
from wiki.common.schemas import BaseResponse, WikiUserHandlerData
from wiki.database.deps import get_db
from wiki.permissions.login import LoginPermission
from wiki.permissions.signup import SignUpPermission
from wiki.user.models import User
from wiki.user.repository import UserRepository
from wiki.user.schemas import CreateUser
from wiki.wiki_email.core import EmailProvider
from wiki.wiki_email.deps import get_email_provider
from wiki.wiki_email.schemas import EmailSchema

auth_router = APIRouter()
wiki_logger = logging.getLogger(__name__)


@auth_router.post(
    "/login",
    response_model=UserSignResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Login by email or username",
    response_description="Verification token data."
)
async def login(user_in: FrontendUserLogin,
                request: Request,
                session: AsyncSession = Depends(get_db),
                permission=Depends(LoginPermission()),
                email_provider: EmailProvider = Depends(get_email_provider)):
    """
    ## Logging in to a user account
    The endpoint for sending an email or username and receiving a login confirmation token.
    A confirmation code will be sent to the specified email.
    """
    authenticator = VerificationCodeAuthenticatorInterface(session)
    code = authenticator.verification_code
    token = authenticator.create_verify_token(VerifyTokenData(
        email=user_in.email,
        user_ip=request.client.host,
        user_agent=request.headers.get("User-Agent"),
        appointment=VerificationType.login),
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
    summary="Signup with user data entry",
    response_description="Verification token data."
)
async def signup(request: Request,
                 session: AsyncSession = Depends(get_db),
                 user_signup=Depends(SignUpPermission()),
                 email_provider: EmailProvider = Depends(get_email_provider)):
    """
    ## Registration - submitting an application
    Sending an application for registration in the system.
    """
    user_repository: UserRepository = UserRepository(session)

    authenticator = VerificationCodeAuthenticatorInterface(session)
    code = authenticator.verification_code
    verify_token = VerificationCodeAuthenticatorInterface.create_verify_token(VerifyTokenData(
        email=user_signup.email,
        user_ip=request.client.host,
        user_agent=request.headers.get("User-Agent"),
        appointment=VerificationType.signup
    ), code)

    user = await user_repository.create_user(CreateUser(
        email=user_signup.email,
        username=user_signup.username,
        first_name=user_signup.first_name,
        last_name=user_signup.last_name,
        second_name=user_signup.second_name,
        user_position=user_signup.user_position,
        organization_id=user_signup.organization_id
    ))

    await email_provider.send_mail(EmailSchema(
        email=[user_signup.email],
        code=code,
        subject="Your verification code to confirm your signup."
    ))

    wiki_logger.info(f"{user_signup.email}: {code}")

    return UserSignResponse(
        email_to=user_signup.email,
        verify_token=verify_token
    )


@auth_router.get(
    "/verify",
    response_model=BaseResponse,
    status_code=status.HTTP_200_OK,
    summary="Verification by token and code",
    response_description="Cookies are set. Success message."
)
async def verify(response: Response,
                 data: VerifyData = Depends(),
                 session: AsyncSession = Depends(get_db)):
    """
    ## Verification on the sent code
    Endpoint for confirming the code received by mail, issuing access token to perform authorized actions.
    """
    authenticator = VerificationCodeAuthenticatorInterface(session, verification_code=data.verification_code)
    data = await authenticator.validate(data.token)
    if isinstance(data, WikiUserHandlerData):
        token = WikiTokenAuthenticatorInterface.create_access_token(AccessTokenData(
            email=data.email,
            api_client_id=str(data.wiki_api_client.id)
        ))

        # response.set_cookie(settings.AUTH_ACCESS_TOKEN_COOKIE_NAME,
        #                     token,
        #                     settings.AUTH_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        #                     settings.AUTH_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        #                     # settings.AUTH_TOKEN_COOKIE_PATH,
        #                     # settings.AUTH_TOKEN_COOKIE_DOMAIN,
        #                     # settings.AUTH_TOKEN_COOKIE_SECURE,
        #                     # settings.AUTH_TOKEN_COOKIE_HTTP_ONLY,
        #                     settings.AUTH_TOKEN_COOKIE_SAME_SITE)

        return BaseResponse(msg=token)
    else:
        email = data
        user_repository: UserRepository = UserRepository(session)
        user: User = await user_repository.get_user_by_email(email)
        user = await user_repository.update_user(user.id, is_verified_email=True)
        return BaseResponse(msg="Successful email verification.")
