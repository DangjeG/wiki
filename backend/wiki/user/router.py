from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from wiki.common.exceptions import WikiException, WikiErrorCode
from wiki.common.schemas import BaseResponse, WikiUserHandlerData
from wiki.database.deps import get_db
from wiki.permissions.base import BasePermission
from wiki.user.models import User
from wiki.user.repository import UserRepository
from wiki.user.schemas import UserInfoResponse, UserIdentifiers, UserUpdate
from wiki.wiki_api_client.enums import ResponsibilityType
from wiki.wiki_api_client.models import WikiApiClient
from wiki.wiki_api_client.repository import WikiApiClientRepository


user_router = APIRouter()


@user_router.get(
    "/me",
    response_model=UserInfoResponse,
    status_code=status.HTTP_200_OK,
    summary="Get info about the current user",
)
async def get_me(
        user: WikiUserHandlerData = Depends(BasePermission(responsibility=ResponsibilityType.VIEWER)),
):
    return UserInfoResponse(
        user_name=user.username,
        email=user.email,
        last_name=user.last_name,
        first_name=user.first_name,
        responsibility=user.wiki_api_client.responsibility
    )


@user_router.get(
    "/info",
    response_model=UserInfoResponse,
    status_code=status.HTTP_200_OK,
    summary="Get user by id or username or email"
)
async def get_user(
        user: WikiUserHandlerData = Depends(BasePermission(responsibility=ResponsibilityType.ADMIN)),
        session: AsyncSession = Depends(get_db),
        user_get: UserIdentifiers = Depends()
):
    wiki_api_client_repository: WikiApiClientRepository = WikiApiClientRepository(session)
    user_repository: UserRepository = UserRepository(session)

    if user_get.user_id is not None:
        user_db = await user_repository.get_user_by_id(user_get.user_id)
    elif user_get.user_name is not None:
        user_db = await user_repository.get_user_by_username(user_get.user_name)
    elif user_get.email is not None:
        user_db = await user_repository.get_user_by_email(str(user_get.email))
    else:
        raise WikiException(
            message=f"User not found.",
            error_code=WikiErrorCode.USER_NOT_FOUND,
            http_status_code=status.HTTP_404_NOT_FOUND
        )

    wiki_api_client_by_id = await wiki_api_client_repository.get_wiki_api_client_by_id(user_db.wiki_api_client_id)

    return UserInfoResponse(
        user_name=user_db.username,
        email=user_db.email,
        last_name=user_db.last_name,
        first_name=user_db.first_name,
        responsibility=wiki_api_client_by_id.responsibility
    )


@user_router.get(
    "/all",
    response_model=list[UserInfoResponse],
    status_code=status.HTTP_200_OK,
    summary="Get all users"
)
async def get_users(
        user: WikiUserHandlerData = Depends(BasePermission(responsibility=ResponsibilityType.ADMIN)),
        session: AsyncSession = Depends(get_db)
):
    client_repository: WikiApiClientRepository = WikiApiClientRepository(session)
    user_repository: UserRepository = UserRepository(session)

    users: list[User] = await user_repository.get_all_users()

    client_users: list[WikiApiClient] = await client_repository.get_all_wiki_api_clients()

    result_users: list[UserInfoResponse] = []

    for us in users:
        for client in client_users:
            if client.id == us.wiki_api_client_id:
                append_user = UserInfoResponse(
                    user_name=us.username,
                    email=us.email,
                    first_name=us.first_name,
                    last_name=us.last_name,
                    second_name=us.second_name,
                    responsibility=client.responsibility)
                result_users.append(append_user)
                break

    return result_users


@user_router.delete(
    "/",
    response_model=BaseResponse,
    status_code=status.HTTP_200_OK,
    summary="Delete user"
)
async def delete_user(
        user: WikiUserHandlerData = Depends(BasePermission(responsibility=ResponsibilityType.ADMIN)),
        user_identifiers: UserIdentifiers = Depends(),
        session: AsyncSession = Depends(get_db)
):
    user_repository: UserRepository = UserRepository(session)

    if user_identifiers.user_id is not None:
        user_db = await user_repository.get_user_by_id(user_identifiers.user_id)
    elif user_identifiers.user_name is not None:
        user_db = await user_repository.get_user_by_username(user_identifiers.user_name)
    elif user_identifiers.email is not None:
        user_db = await user_repository.get_user_by_email(user_identifiers.email)
    else:
        raise WikiException(
            message=f"User not found",
            error_code=WikiErrorCode.USER_NOT_FOUND,
            http_status_code=status.HTTP_404_NOT_FOUND
        )

    msg = f"User id: {user_db.id} username: {user_db.username}, email: {user_db.email} deleted"
    await user_repository.mark_user_deleted(user_db.id)

    return BaseResponse(
        msg=msg
    )


@user_router.put(
    "/",
    response_model=UserUpdate,
    status_code=status.HTTP_200_OK,
    summary="Update user"
)
async def update_user(user: WikiUserHandlerData = Depends(BasePermission(responsibility=ResponsibilityType.ADMIN)),
                      session: AsyncSession = Depends(get_db),
                      user_identifiers: UserIdentifiers = Depends(),
                      user_update: UserUpdate = Depends()):
    user_repository: UserRepository = UserRepository(session)

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

    updated_user = await user_repository.update_user(
        user.id,
        email=user_update.email,
        username=user_update.username,
        display_name=user_update.display_name,
        first_name=user_update.first_name,
        last_name=user_update.last_name,
        second_name=user_update.second_name,
        position=user_update.user_position,
        organization_id=user_update.organization_id,
        wiki_api_client_id=user_update.wiki_api_client_id
    )

    return updated_user
