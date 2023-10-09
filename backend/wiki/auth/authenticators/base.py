import time
from datetime import timedelta
from enum import Enum
from uuid import UUID

from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from wiki.auth.schemas import UserHandlerData
from wiki.common.exceptions import WikiException, WikiErrorCode
from wiki.config import settings
from wiki.database.utils import utcnow
from wiki.organization.enums import OrganizationAccessType
from wiki.organization.models import Organization
from wiki.organization.repository import OrganizationRepository
from wiki.user.models import User
from wiki.user.repository import UserRepository
from wiki.wiki_api_client.models import WikiApiClient
from wiki.wiki_api_client.repository import WikiApiClientRepository


class AuthenticatorType(str, Enum):
    api_key = "api_key"
    token = "token"
    verification_code = "verification_code"


class AuthenticatorInterface:
    authenticator_type: AuthenticatorType

    session: AsyncSession
    api_client_repository: WikiApiClientRepository
    user_repository: UserRepository
    organization_repository: OrganizationRepository

    def __init__(self, session: AsyncSession):
        self.session = session
        self.api_client_repository = WikiApiClientRepository(session)
        self.user_repository = UserRepository(session)
        self.organization_repository = OrganizationRepository(session)

    async def verify_api_client(self, api_client_id: UUID) -> WikiApiClient:
        wiki_api_client: WikiApiClient = await self.api_client_repository.get_wiki_api_client_by_id(api_client_id)
        if wiki_api_client.is_deleted or not wiki_api_client.is_enabled:
            raise WikiException(
                message="Api client credentials is not valid or expired.",
                error_code=WikiErrorCode.AUTH_API_CLIENT_NOT_FOUND,
                http_status_code=status.HTTP_403_FORBIDDEN
            )

        return wiki_api_client

    async def verify_user(self, api_client: WikiApiClient) -> User:
        user: User = await self.user_repository.get_user_by_wiki_api_client_id(api_client.id)
        if user.is_deleted:
            raise WikiException(
                message="User credentials is not valid or expired.",
                error_code=WikiErrorCode.AUTH_USER_NOT_FOUND,
                http_status_code=status.HTTP_403_FORBIDDEN
            )
        organization = None
        if user.organization_id is not None:
            organization: Organization = self.organization_repository.get_organization_by_id(user.organization_id)
            if self.authenticator_type == AuthenticatorType.api_key:
                if organization.access != OrganizationAccessType.FULL_ACCESS:
                    raise WikiException(
                        message="The organization you are a member of does not have access to API keys.",
                        error_code=WikiErrorCode.AUTH_ORGANIZATION_NOT_ACCESS_API,
                        http_status_code=status.HTTP_403_FORBIDDEN
                    )
            if organization.access == OrganizationAccessType.LOCKED:
                raise WikiException(
                    message="The organization you are a member of does not have access to Wiki service.",
                    error_code=WikiErrorCode.AUTH_ORGANIZATION_NOT_ACCESS,
                    http_status_code=status.HTTP_403_FORBIDDEN
                )

        return user, organization

    async def validate(self, credentials) -> UserHandlerData:
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
