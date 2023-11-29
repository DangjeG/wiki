from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi_pagination import Page, paginate
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from wiki.common.exceptions import WikiException, WikiErrorCode
from wiki.common.schemas import WikiUserHandlerData, BaseResponse
from wiki.database.deps import get_db
from wiki.permissions.base import BasePermission
from wiki.user.repository import UserRepository
from wiki.user.schemas import UserBaseInfoResponse, UserIdentifiers
from wiki.user.utils import get_user_info, get_user_db_by_user_identifiers
from wiki.user_group.repository import GroupRepository
from wiki.user_group.schemas import CreateGroup, GroupInfo, GroupInfoWithUsers, GroupOptionalInfo
from wiki.wiki_api_client.enums import ResponsibilityType


user_group_router = APIRouter()


@user_group_router.post(
    "/",
    response_model=GroupInfo,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Create user group"
)
async def create_user_group(
        create_group: CreateGroup,
        user: WikiUserHandlerData = Depends(BasePermission(responsibility=ResponsibilityType.EDITOR)),
        session: AsyncSession = Depends(get_db)
):
    """
    ## Create user group
    Available for users starting from the EDITOR responsibility level
    """

    group_repository = GroupRepository(session)
    group = await group_repository.create_group(create_group)

    return group.get_group_info()


@user_group_router.put(
    "/info",
    response_model=GroupInfo,
    status_code=status.HTTP_200_OK,
    summary="Update group info by id"
)
async def update_user_group_info(
        group_id: UUID,
        update_group: GroupOptionalInfo,
        user: WikiUserHandlerData = Depends(BasePermission(responsibility=ResponsibilityType.EDITOR)),
        session: AsyncSession = Depends(get_db)
):
    group_repository = GroupRepository(session)
    group = await group_repository.update_group(group_id, update_group)

    return group.get_group_info()


@user_group_router.delete(
    "/",
    response_model=BaseResponse,
    status_code=status.HTTP_200_OK,
    summary="Delete group info by id"
)
async def delete_user_group(
        group_id: UUID,
        user: WikiUserHandlerData = Depends(BasePermission(responsibility=ResponsibilityType.EDITOR)),
        session: AsyncSession = Depends(get_db)
):
    group_repository = GroupRepository(session)
    await group_repository.delete_group(group_id)

    return BaseResponse(msg="Group has been deleted")


@user_group_router.get(
    "/info",
    response_model=GroupInfo,
    status_code=status.HTTP_200_OK,
    summary="Get user group info by id"
)
async def get_user_group_info(
        group_id: UUID,
        user: WikiUserHandlerData = Depends(BasePermission(responsibility=ResponsibilityType.VIEWER)),
        session: AsyncSession = Depends(get_db)
):
    """
    ## Get user group info by id
    Get base information without group members
    """

    group_repository = GroupRepository(session)
    group = await group_repository.get_group_by_id(group_id)

    return group.get_group_info()


@user_group_router.get(
    "/full-info",
    response_model=GroupInfoWithUsers,
    status_code=status.HTTP_200_OK,
    summary="Get user group info with members by id"
)
async def get_user_group_full_info(
        group_id: UUID,
        user: WikiUserHandlerData = Depends(BasePermission(responsibility=ResponsibilityType.VIEWER)),
        session: AsyncSession = Depends(get_db)
):
    """
    ## Get user group info with members by id
    Get information about the group and all its members
    """

    group_repository = GroupRepository(session)
    group = await group_repository.get_group_by_id(group_id)
    members = await group_repository.get_members_users_group(group)

    return group.get_group_info_with_members([await get_user_info(member, session) for member in members])


@user_group_router.get(
    "/members",
    response_model=Page[UserBaseInfoResponse],
    status_code=status.HTTP_200_OK,
    summary="Get members group by id"
)
async def get_members_user_group(
        group_id: UUID,
        user: WikiUserHandlerData = Depends(BasePermission(responsibility=ResponsibilityType.VIEWER)),
        session: AsyncSession = Depends(get_db)
):
    group_repository = GroupRepository(session)
    group = await group_repository.get_group_by_id(group_id)
    members = await group_repository.get_members_users_group(group)

    return paginate([await get_user_info(member, session) for member in members])


@user_group_router.get(
    "/all",
    response_model=Page[GroupInfo],
    status_code=status.HTTP_200_OK,
    summary="Get all groups info"
)
async def get_all_groups_info(
        filter_group: GroupOptionalInfo = Depends(GroupOptionalInfo),
        user: WikiUserHandlerData = Depends(BasePermission(responsibility=ResponsibilityType.VIEWER)),
        session: AsyncSession = Depends(get_db)
):
    group_repository = GroupRepository(session)
    groups = await group_repository.get_all_groups_filter(filter_group)

    return paginate([group.get_group_info() for group in groups])


@user_group_router.get(
    "/all/full-info",
    response_model=Page[GroupInfoWithUsers],
    status_code=status.HTTP_200_OK,
    summary="Get all groups info with members"
)
async def get_all_groups_full_info(
        filter_group: GroupOptionalInfo = Depends(GroupOptionalInfo),
        user: WikiUserHandlerData = Depends(BasePermission(responsibility=ResponsibilityType.VIEWER)),
        session: AsyncSession = Depends(get_db)
):
    group_repository = GroupRepository(session)
    groups = await group_repository.get_all_groups_filter(filter_group)

    return paginate([
        group.get_group_info_with_members(
            [await get_user_info(member, session) for member in await group_repository.get_members_users_group(group)]
        ) for group in groups
    ])


@user_group_router.get(
    "/user/info",
    response_model=Page[GroupInfo],
    status_code=status.HTTP_200_OK,
    summary="Get groups info for user"
)
async def get_groups_info_for_user(
        user_identifiers: UserIdentifiers = Depends(),
        filter_group: GroupOptionalInfo = Depends(GroupOptionalInfo),
        user: WikiUserHandlerData = Depends(BasePermission(responsibility=ResponsibilityType.VIEWER)),
        session: AsyncSession = Depends(get_db)
):
    user_repository: UserRepository = UserRepository(session)
    user_db = await get_user_db_by_user_identifiers(user_identifiers, user_repository)

    group_repository = GroupRepository(session)
    groups = await group_repository.get_groups_for_user(user_db, filter_group)

    return paginate([group.get_group_info() for group in groups])


@user_group_router.get(
    "/user/full-info",
    response_model=Page[GroupInfoWithUsers],
    status_code=status.HTTP_200_OK,
    summary="Get groups info for user with members"
)
async def get_groups_full_info_for_user(
        user_identifiers: UserIdentifiers = Depends(),
        filter_group: GroupOptionalInfo = Depends(GroupOptionalInfo),
        user: WikiUserHandlerData = Depends(BasePermission(responsibility=ResponsibilityType.VIEWER)),
        session: AsyncSession = Depends(get_db)
):
    user_repository: UserRepository = UserRepository(session)
    user_db = await get_user_db_by_user_identifiers(user_identifiers, user_repository)

    group_repository = GroupRepository(session)
    groups = await group_repository.get_groups_for_user(user_db, filter_group)

    return paginate([
        group.get_group_info_with_members(
            [await get_user_info(member, session) for member in await group_repository.get_members_users_group(group)]
        ) for group in groups
    ])


@user_group_router.post(
    "/member",
    response_model=BaseResponse,
    status_code=status.HTTP_200_OK,
    summary="Add member user for group"
)
async def add_member_group(
        group_id: UUID,
        user_identifiers: UserIdentifiers = Depends(),
        user: WikiUserHandlerData = Depends(BasePermission(responsibility=ResponsibilityType.VIEWER)),
        session: AsyncSession = Depends(get_db)
):
    user_repository: UserRepository = UserRepository(session)
    user_db = await get_user_db_by_user_identifiers(user_identifiers, user_repository)

    group_repository = GroupRepository(session)
    group = await group_repository.get_group_by_id(group_id)
    if user.wiki_api_client.responsibility >= ResponsibilityType.EDITOR or group.is_members_can_add_to_group:
        await group_repository.add_user_in_group(group, user_db)
    else:
        raise WikiException(
            message="You can't add a member to the group",
            error_code=WikiErrorCode.USER_ADD_MEMBER_GROUP_FORBIDDEN,
            http_status_code=status.HTTP_403_FORBIDDEN
        )

    return BaseResponse(msg="Member has been added to the group")


@user_group_router.delete(
    "/member",
    response_model=BaseResponse,
    status_code=status.HTTP_200_OK,
    summary="Remove member user from group"
)
async def remove_member_group(
        group_id: UUID,
        user_identifiers: UserIdentifiers = Depends(),
        user: WikiUserHandlerData = Depends(BasePermission(responsibility=ResponsibilityType.EDITOR)),
        session: AsyncSession = Depends(get_db)
):
    user_repository: UserRepository = UserRepository(session)
    user_db = await get_user_db_by_user_identifiers(user_identifiers, user_repository)

    group_repository = GroupRepository(session)
    await group_repository.remove_user_from_group(group_id, user_db)

    return BaseResponse(msg="Member has been removed from group")
