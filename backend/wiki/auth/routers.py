from fastapi import APIRouter, Security, Request
from starlette import status

from wiki.auth.core import create_verify_token, create_access_token, WikiBearer
from wiki.auth.deps import bearer_token
from wiki.auth.schemas import UserLogin, UserLoginResponse, VerifyTokenData, UserVerifyResponse, AccessTokenData, \
    VerifyData

auth_router = APIRouter()


@auth_router.post(
    "/login",
    response_model=UserLoginResponse,
    status_code=status.HTTP_202_ACCEPTED,
    description="The endpoint for sending an email and receiving a login confirmation token."
                "A confirmation code will be sent to the specified email."
)
async def login(user_in: UserLogin, request: Request):
    verification_code, token = create_verify_token(VerifyTokenData(
        email=user_in.email,
        user_ip=request.client.host,
        user_agent=request.headers.get("User-Agent"))
    )
    print(f"\n{verification_code}\n")
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
