from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from wiki.auth.resolvers.base import Resolver
from wiki.auth.schemas import FrontendUserLogin
from wiki.common.exceptions import WikiException, WikiErrorCode
from wiki.user.models import User
from wiki.user.repository import UserRepository
from wiki.wiki_api_client.models import WikiApiClient
from wiki.wiki_api_client.repository import WikiApiClientRepository


class UserLoginResolver(Resolver):
    user_repository: UserRepository
    api_client_repository: WikiApiClientRepository

    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.user_repository = UserRepository(session)
        self.api_client_repository = WikiApiClientRepository(session)

    async def resolve(self, candidate: FrontendUserLogin) -> bool:
        if candidate.email is not None:
            user: User = await self.user_repository.get_user_by_email(candidate.email)
        elif candidate.username is not None:
            user: User = await self.user_repository.get_user_by_username(candidate.username)
        else:
            raise WikiException(
                message="Could not validate credentials.",
                error_code=WikiErrorCode.AUTH_NOT_VALIDATE_CREDENTIALS,
                http_status_code=status.HTTP_401_UNAUTHORIZED
            )

        api_client_id = user.wiki_api_client_id
        if api_client_id is not None:
            api_client: WikiApiClient = await self.api_client_repository.get_wiki_api_client_by_id(api_client_id)
            if not api_client.is_deleted and api_client.is_enabled:
                return True

        raise WikiException(
            message="You do not have access or have not been approved.",
            error_code=WikiErrorCode.AUTH_NOT_ACCESS,
            http_status_code=status.HTTP_403_FORBIDDEN
        )
