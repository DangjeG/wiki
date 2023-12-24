from typing import Optional
from uuid import UUID

from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from wiki.auth.authenticators.base import AuthenticatorType, BaseTokenAuthenticatorInterface
from wiki.auth.schemas import AccessTokenData
from wiki.common.exceptions import WikiException, WikiErrorCode
from wiki.common.schemas import WikiUserHandlerData
from wiki.config import settings
from wiki.wiki_api_client.schemas import WikiApiClientInfoResponse


class WikiTokenAuthenticatorInterface(BaseTokenAuthenticatorInterface):
    _token_no_valid_or_expire_exception = WikiException(
        message="Token is not valid or expired.",
        error_code=WikiErrorCode.AUTH_TOKEN_NOT_VALID_OR_EXPIRED,
        http_status_code=status.HTTP_403_FORBIDDEN
    )

    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.authenticator_type = AuthenticatorType.token

    @classmethod
    async def verify_jwt_token(cls, token: str) -> (Optional[UUID], Optional[str]):
        payload = cls.decode_jwt_token(token, settings.AUTH_SECRET_MAIN)
        if payload is None:
            raise cls._token_no_valid_or_expire_exception
        api_client_id = payload.get("api_client_id")
        email = payload.get("email")

        return api_client_id, email

    @classmethod
    def create_access_token(cls, data: AccessTokenData) -> str:
        encoded_jwt = jwt.encode(cls._get_token_claims(data.model_dump(), settings.AUTH_ACCESS_TOKEN_EXPIRE_MINUTES),
                                 settings.AUTH_SECRET_MAIN,
                                 algorithm=settings.AUTH_ALGORITHM)
        return encoded_jwt

    async def validate(self, credentials, is_available_disapproved_user: bool) -> WikiUserHandlerData:
        api_client_id, user_email = await self.verify_jwt_token(credentials)
        if api_client_id is None and not is_available_disapproved_user:
            raise self._token_no_valid_or_expire_exception
        api_client = None
        if not is_available_disapproved_user:
            api_client = await self.verify_api_client(api_client_id)
            user = await self.verify_user(api_client=api_client)
        else:
            user = await self.verify_user(user_email=user_email)

        return WikiUserHandlerData(
            id=user.id,
            email=user.email,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            second_name=user.second_name,
            position=user.position,
            wiki_api_client=api_client.get_response_info() if api_client is not None else None
        )
