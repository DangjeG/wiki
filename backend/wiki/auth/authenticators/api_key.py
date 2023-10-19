import binascii
import hmac
import os
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from wiki.auth.authenticators.base import AuthenticatorInterface, AuthenticatorType
from wiki.common.exceptions import WikiException, WikiErrorCode
from wiki.common.schemas import WikiUserHandlerData
from wiki.config import settings
from wiki.database.utils import utcnow
from wiki.wiki_api_client.models import WikiApiKey


class ApiKeyAuthenticatorInterface(AuthenticatorInterface):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.authenticator_type = AuthenticatorType.api_key

    @classmethod
    def get_api_key_hash(cls, api_key: str) -> str:
        return hmac.new(settings.AUTH_SECRET_API_KEY,
                        api_key.encode(encoding="utf-8"),
                        settings.AUTH_ALGORITHM_API_KEY).hexdigest()

    @classmethod
    def generate_api_key(cls):
        return binascii.b2a_hex(os.urandom(settings.AUTH_API_KEY_LENGTH)).decode(encoding="utf-8")

    async def verify_api_key(self, api_key) -> UUID:
        generated_hash = self.get_api_key_hash(api_key)
        wiki_api_key: WikiApiKey = await self.api_client_repository.get_wiki_api_key_by_key_hash(generated_hash)
        if wiki_api_key.is_enabled or wiki_api_key.is_deleted or utcnow() > wiki_api_key.expires_date:
            raise WikiException(
                message="API key is not valid or expired.",
                error_code=WikiErrorCode.AUTH_API_KEY_NOT_VALID_OR_EXPIRED,
                http_status_code=status.HTTP_403_FORBIDDEN
            )

        return wiki_api_key.owner_id

    async def validate(self, credentials, is_available_disapproved_user: bool) -> WikiUserHandlerData:
        api_client_id = await self.verify_api_key(credentials)
        api_client = await self.verify_api_client(api_client_id)
        user, organization = await self.verify_user(api_client)

        return WikiUserHandlerData(
            id=user.id,
            email=user.email,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            second_name=user.second_name,
            position=user.position,
            organization=organization,
            wiki_api_client=api_client
        )
