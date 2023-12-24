from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from wiki.common.exceptions import WikiException, WikiErrorCode
from wiki.common.schemas import WikiUserHandlerData
from wiki.user.models import User
from wiki.user.repository import UserRepository
from wiki.user.schemas import UserFullInfoResponse, UserBaseInfoResponse, UserIdentifiers
from wiki.wiki_api_client.models import WikiApiClient
from wiki.wiki_api_client.repository import WikiApiClientRepository
from wiki.wiki_api_client.schemas import WikiApiClientInfoResponse


async def get_user_info(
        user: User | WikiUserHandlerData | UUID,
        session: AsyncSession,
        is_full: bool = True
) -> UserFullInfoResponse | UserBaseInfoResponse:
    wiki_api_client_response: Optional[WikiApiClientRepository] = None

    user_repository: UserRepository = UserRepository(session)
    if isinstance(user, User):
        pass
    elif isinstance(user, WikiUserHandlerData):
        user = await user_repository.get_user_by_id(user.id)
    else:
        user = await user_repository.get_user_by_id(user)

    if user.wiki_api_client_id is not None:
        wiki_api_client_repository: WikiApiClientRepository = WikiApiClientRepository(session)
        wiki_api_client: WikiApiClient = await wiki_api_client_repository.get_wiki_api_client_by_id(
            user.wiki_api_client_id)
        wiki_api_client_response = WikiApiClientInfoResponse(
            id=wiki_api_client.id,
            description=wiki_api_client.description,
            responsibility=wiki_api_client.responsibility,
            is_enabled=wiki_api_client.is_enabled
        )

    kwargs = {
        "email": user.email,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "second_name": user.second_name,
        "position": user.position,
        "wiki_api_client": wiki_api_client_response
    }

    if is_full:
        return UserFullInfoResponse(
            **kwargs,
            is_user_agreement_accepted=user.is_user_agreement_accepted,
            is_verified_email=user.is_verified_email,
            is_enabled=user.is_enabled
        )
    else:
        return UserBaseInfoResponse(**kwargs)


async def get_user_db_by_user_identifiers(user_identifiers: UserIdentifiers, user_repository: UserRepository) -> User:
    if user_identifiers.user_id is not None:
        user_db = await user_repository.get_user_by_id(user_identifiers.user_id)
    elif user_identifiers.username is not None:
        user_db = await user_repository.get_user_by_username(user_identifiers.username)
    elif user_identifiers.email is not None:
        user_db = await user_repository.get_user_by_email(user_identifiers.email)
    else:
        raise WikiException(
            message=f"User not found",
            error_code=WikiErrorCode.USER_NOT_FOUND,
            http_status_code=status.HTTP_404_NOT_FOUND
        )

    return user_db
