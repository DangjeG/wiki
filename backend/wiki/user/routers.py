from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from wiki.common.exceptions import WikiException, WikiErrorCode
from wiki.common.schemas import BaseResponse
from wiki.database.deps import get_db
from wiki.user.models import User
from wiki.user.repository import UserRepository
from wiki.user.schemas import UserInfoResponse, UserIdentifiers
from wiki.wiki_api_client.models import WikiApiClient
from wiki.wiki_api_client.repository import WikiApiClientRepository

user_router = APIRouter()

@user_router.get(
    "/info",
    response_model=UserInfoResponse,
    status_code=status.HTTP_200_OK,
    description="Get user by id or username or email."
)
async def get_user(session: AsyncSession = Depends(get_db),
             user_get: UserIdentifiers = Depends()):

    wiki_api_client_repository: WikiApiClientRepository = WikiApiClientRepository(session)
    user_repository: UserRepository = UserRepository(session)

    user: Optional[User] = None

    if user_get.user_id is not None:
        user = await user_repository.get_user_by_id(user_get.user_id)
    elif user_get.user_name is not None:
        user = await user_repository.get_user_by_username(user_get.user_name)
    elif user_get.email is not None:
        user = await user_repository.get_user_by_email(user_get.email)
    else:
        raise WikiException(
            message=f"User not found",
            error_code=WikiErrorCode.USER_NOT_FOUND,
            http_status_code=status.HTTP_404_NOT_FOUND
        )

    wiki_api_client_by_id = await wiki_api_client_repository.get_wiki_api_client_by_id(user.id)

    return UserInfoResponse(
        user_name=user.username,
        email=user.email,
        last_name=user.last_name,
        first_name=user.first_name,
        responsibility=wiki_api_client_by_id.responsibility
    )

@user_router.get(
    "/",
    response_model=list[UserInfoResponse],
    status_code=status.HTTP_200_OK,
    description="Get users."
)
async def get_users(session: AsyncSession = Depends(get_db)):
    client_repository: WikiApiClientRepository = WikiApiClientRepository(session)
    user_repository: UserRepository = UserRepository(session)

    users: list[User] = await user_repository.get_all_users()

    client_users: list[WikiApiClient] = await client_repository.get_all_wiki_api_clients()

    result_users: list[UserInfoResponse] = []

    for user in users:
        for client in client_users:
            if client.id == user.id:
                append_user = UserInfoResponse(
                    user_name=user.username,
                    email=user.email,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    second_name=user.second_name,
                    responsibility=client.responsibility)
                result_users.append(append_user)
                break

    return result_users

@user_router.delete(
    "/",
    response_model=BaseResponse,
    status_code=status.HTTP_200_OK,
    description="Delete users."
)
async def delete_user(user_identifiers: UserIdentifiers = Depends(),
                session: AsyncSession = Depends(get_db)):
    user_repository: UserRepository = UserRepository(session)

    user: Optional[User] = None

    if user_identifiers.user_id is not None:
        user = await user_repository.get_user_by_id(user_identifiers.user_id)
    elif user_identifiers.user_name is not None:
        user = await user_repository.get_user_by_username(user_identifiers.user_name)
    elif user_identifiers.email is not None:
        user = await user_repository.get_user_by_email(user_identifiers.email)
    else:
        raise WikiException(
            message=f"User not found",
            error_code=WikiErrorCode.USER_NOT_FOUND,
            http_status_code=status.HTTP_404_NOT_FOUND
        )

    await user_repository.mark_user_deleted(user.id)

    return BaseResponse(
        msg=f"User id: {user.id} username: {user.username}, email: {user.email} deleted"
    )
