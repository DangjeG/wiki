from uuid import UUID

from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from wiki.auth.authenticators.base import AuthenticatorType, BaseTokenAuthenticatorInterface
from wiki.auth.schemas import UserHandlerData, AccessTokenData
from wiki.common.exceptions import WikiException, WikiErrorCode
from wiki.config import settings


class WikiTokenAuthenticatorInterface(BaseTokenAuthenticatorInterface):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.authenticator_type = AuthenticatorType.token

    @classmethod
    async def verify_jwt_token(cls, token: str) -> UUID:
        payload = cls.decode_jwt_token(token, settings.AUTH_SECRET_MAIN)
        ex = WikiException(
            message="Token is not valid or expired.",
            error_code=WikiErrorCode.AUTH_TOKEN_NOT_VALID_OR_EXPIRED,
            http_status_code=status.HTTP_403_FORBIDDEN
        )
        if payload is None:
            raise ex
        api_client_id = payload.get("api_client_id")
        if api_client_id is None:
            raise ex

        return api_client_id

    @classmethod
    def create_access_token(cls, data: AccessTokenData) -> str:
        encoded_jwt = jwt.encode(cls._get_token_claims(data.model_dump(), settings.AUTH_ACCESS_TOKEN_EXPIRE_MINUTES),
                                 settings.AUTH_SECRET_MAIN,
                                 algorithm=settings.AUTH_ALGORITHM)
        return encoded_jwt

    async def validate(self, credentials) -> UserHandlerData:
        api_client_id = await self.verify_jwt_token(credentials)
        api_client = await self.verify_api_client(api_client_id)
        user, organization = await self.verify_user(api_client)

        return UserHandlerData(
            id=user.id,
            email=user.email,
            username=user.username,
            display_name=user.display_name,
            first_name=user.first_name,
            last_name=user.last_name,
            second_name=user.second_name,
            position=user.position,
            organization=organization,
            wiki_api_client=api_client
        )
