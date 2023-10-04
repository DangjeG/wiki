import logging

from fastapi import APIRouter, Security, Request, Depends
from starlette import status

from wiki.auth.core import create_verify_token, create_access_token, WikiBearer
from wiki.auth.deps import bearer_token
from wiki.auth.schemas import UserLogin, UserLoginResponse, VerifyTokenData, UserVerifyResponse, AccessTokenData, \
    VerifyData
from wiki.config import settings
from wiki.emile.core import EmailProvider
from wiki.emile.deps import get_email_provider
from wiki.emile.schemas import EmailSchema

auth_router = APIRouter()
wiki_logger = logging.getLogger(settings.LOGGER_NAME)


@auth_router.post(
    "/login",
    response_model=UserLoginResponse,
    status_code=status.HTTP_202_ACCEPTED,
    description="The endpoint for sending an email and receiving a login confirmation token."
                "A confirmation code will be sent to the specified email."
)
async def login(user_in: UserLogin, request: Request, email_provider: EmailProvider = Depends(get_email_provider)):
    verification_code, token = create_verify_token(VerifyTokenData(
        email=user_in.email,
        user_ip=request.client.host,
        user_agent=request.headers.get("User-Agent"))
    )
    await email_provider.send_mail(EmailSchema(
        email=[user_in.email],
        code=verification_code,
        subject="Your verification code to log in to the Wiki."
    ))
    wiki_logger.info(f"{user_in.email}: {verification_code}")
    return UserLoginResponse(email_to=user_in.email, verify_token=token)


@auth_router.post(
    "/verify",
    response_model=UserVerifyResponse,
    status_code=status.HTTP_200_OK,
    description="Endpoint for confirming the code received by mail, issuing access token to perform authorized actions."
)
async def verify(data: VerifyData):
    payload = WikiBearer.verify_verification_token(data.token, data.code)
    access_token = create_access_token(AccessTokenData(email=payload.get("email")))
    return UserVerifyResponse(access_token=access_token)


@auth_router.post(
    "/test",
    status_code=status.HTTP_200_OK,
    description="Test endpoint to test the access token."
)
async def test(payload: dict = Security(bearer_token)):
    return f"You have accessed a secure endpoint.. Your email: {payload.get('email')}"
