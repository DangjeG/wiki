import logging

from fastapi import APIRouter, Request, Response, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from wiki.auth.authenticators.verification_code import VerificationCodeAuthenticatorInterface
from wiki.auth.authenticators.wiki_token import WikiTokenAuthenticatorInterface
from wiki.auth.resolvers.email import EmailResolver
from wiki.auth.resolvers.user_login import UserLoginResolver
from wiki.auth.schemas import (
    FrontendUserLogin,
    UserSignResponse,
    VerifyTokenData,
    AccessTokenData,
    VerifyData,
    UserHandlerData,
    VerificationType
)
from wiki.common.exceptions import WikiException, WikiErrorCode
from wiki.common.schemas import BaseResponse
from wiki.config import settings
from wiki.database.deps import get_db
from wiki.user.models import User
from wiki.user.repository import UserRepository
from wiki.user.schemas import CreateUser
from wiki.wiki_api_client.enums import ResponsibilityType
from wiki.wiki_api_client.models import WikiApiClient
from wiki.wiki_api_client.repository import WikiApiClientRepository
from wiki.wiki_api_client.schemas import CreateWikiApiClient
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
                email_provider: EmailProvider = Depends(get_email_provider)):
    """
    ## Logging in to a user account
    The endpoint for sending an email or username and receiving a login confirmation token.
    A confirmation code will be sent to the specified email.
    """
    user_login_resolver = UserLoginResolver(session)
    await user_login_resolver.resolve(user_in)
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
async def signup(user_signup: CreateUser,
                 request: Request,
                 session: AsyncSession = Depends(get_db),
                 email_provider: EmailProvider = Depends(get_email_provider)):
    """
    ## Registration - submitting an application
    Sending an application for registration in the system.
    """
    user_repository: UserRepository = UserRepository(session)
    is_available: bool = await user_repository.check_user_identification_data_is_available(user_signup.email,
                                                                                           user_signup.username)
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
    is_accept_now = await email_resolver.resolve(user_signup.email)

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
        display_name=user_signup.display_name,
        first_name=user_signup.first_name,
        last_name=user_signup.last_name,
        second_name=user_signup.second_name,
        position=user_signup.position,
        organization_id=user_signup.organization_id
    ))

    if is_accept_now:
        api_client_repository = WikiApiClientRepository(session)
        new_api_client: WikiApiClient = await api_client_repository.create_wiki_api_client(CreateWikiApiClient(
            description="Wiki Api client.",
            responsibility=ResponsibilityType.VIEWER,
            is_enabled=True
        ))
        await user_repository.update_user(user.id, wiki_api_client_id=new_api_client.id)

        await email_provider.send_mail(EmailSchema(
            email=[user_signup.email],
            code=code,
            subject="You automatically accessed the system. "
                    "Your verification code to confirm your signup."
        ))
    else:
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
    if isinstance(data, UserHandlerData):
        token = WikiTokenAuthenticatorInterface.create_access_token(AccessTokenData(
            email=data.email,
            api_client_id=str(data.wiki_api_client.id)
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

        return BaseResponse(msg="Successful login.")
    else:
        email = data
        user_repository: UserRepository = UserRepository(session)
        user: User = await user_repository.get_user_by_email(email)
        user = await user_repository.update_user(user.id, is_verified_email=True)
        return BaseResponse(msg="Successful email verification.")
