import time
from datetime import timedelta
from enum import Enum
from typing import Optional
from uuid import UUID

from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from wiki.common.exceptions import WikiException, WikiErrorCode
from wiki.common.schemas import WikiUserHandlerData
from wiki.config import settings
from wiki.database.utils import utcnow
from wiki.user.models import User
from wiki.user.repository import UserRepository
from wiki.wiki_api_client.models import WikiApiClient
from wiki.wiki_api_client.repository import WikiApiClientRepository


class AuthenticatorType(str, Enum):
    api_key = "api_key"
    token = "token"
    verification_code = "verification_code"


class AuthenticatorInterface:
    _credentials_not_valid_or_expired_exception = WikiException(
        message="User credentials is not valid or expired.",
        error_code=WikiErrorCode.AUTH_USER_NOT_FOUND,
        http_status_code=status.HTTP_403_FORBIDDEN
    )

    authenticator_type: AuthenticatorType

    session: AsyncSession
    api_client_repository: WikiApiClientRepository
    user_repository: UserRepository

    def __init__(self, session: AsyncSession):
        self.session = session
        self.api_client_repository = WikiApiClientRepository(session)
        self.user_repository = UserRepository(session)

    async def verify_api_client(self, api_client_id: UUID) -> WikiApiClient:
        wiki_api_client: WikiApiClient = await self.api_client_repository.get_wiki_api_client_by_id(api_client_id)
        if wiki_api_client.is_deleted or not wiki_api_client.is_enabled:
            raise WikiException(
                message="Api client credentials is not valid or expired.",
                error_code=WikiErrorCode.AUTH_API_CLIENT_NOT_FOUND,
                http_status_code=status.HTTP_403_FORBIDDEN
            )

        return wiki_api_client

    async def verify_user(self,
                          api_client: Optional[WikiApiClient] = None,
                          user_email: Optional[str] = None) -> User:
        if api_client is not None:
            user: User = await self.user_repository.get_user_by_wiki_api_client_id(api_client.id)
        elif user_email is not None:
            user: User = await self.user_repository.get_user_by_email(user_email)
        else:
            raise self._credentials_not_valid_or_expired_exception
        if user.is_deleted:
            raise self._credentials_not_valid_or_expired_exception

        return user

    async def validate(self, credentials, is_available_disapproved_user: bool) -> WikiUserHandlerData:
        pass


class BaseTokenAuthenticatorInterface(AuthenticatorInterface):
    @classmethod
    def decode_jwt_token(cls, token: str, secret: str) -> dict:
        try:
            decoded_token: dict = jwt.decode(token, secret, algorithms=settings.AUTH_ALGORITHM)
            exp = decoded_token.get("exp")
            if exp is not None and exp >= time.time():
                return decoded_token
            else:
                return None
        except JWTError:
            return None

    @classmethod
    def _get_token_claims(cls, data: dict, expire_minutes: int):
        expires_delta = timedelta(minutes=expire_minutes)
        to_encode = data.copy()
        expire = utcnow() + expires_delta
        to_encode.update({"exp": expire})
        return to_encode
