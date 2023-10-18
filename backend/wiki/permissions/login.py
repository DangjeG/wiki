from abc import ABC

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from wiki.auth.schemas import FrontendUserLogin
from wiki.common.exceptions import WikiException, WikiErrorCode
from wiki.database.deps import get_db
from wiki.user.models import User
from wiki.user.repository import UserRepository
from wiki.wiki_api_client.models import WikiApiClient
from wiki.wiki_api_client.repository import WikiApiClientRepository


class LoginPermission(ABC):
    async def __call__(self, user_in: FrontendUserLogin, session: AsyncSession = Depends(get_db)):
        user_repository = UserRepository(session)
        # api_client_repository = WikiApiClientRepository(session)

        if user_in.email is not None:
            user: User = await user_repository.get_user_by_email(user_in.email)
        elif user_in.username is not None:
            user: User = await user_repository.get_user_by_username(user_in.username)
        else:
            raise WikiException(
                message="Could not validate credentials.",
                error_code=WikiErrorCode.AUTH_NOT_VALIDATE_CREDENTIALS,
                http_status_code=status.HTTP_401_UNAUTHORIZED
            )

        return True
        # api_client_id = user.wiki_api_client_id
        # if api_client_id is not None:
        #     api_client: WikiApiClient = await api_client_repository.get_wiki_api_client_by_id(api_client_id)
        #     if not api_client.is_deleted and api_client.is_enabled:
        #         return True
        #
        # raise WikiException(
        #     message="You do not have access or have not been approved.",
        #     error_code=WikiErrorCode.AUTH_NOT_ACCESS,
        #     http_status_code=status.HTTP_403_FORBIDDEN
        # )
