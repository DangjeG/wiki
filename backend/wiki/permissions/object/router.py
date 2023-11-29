from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from wiki.common.exceptions import WikiException, WikiErrorCode
from wiki.common.schemas import WikiUserHandlerData
from wiki.database.deps import get_db
from wiki.permissions.base import BasePermission
from wiki.permissions.object.base import BaseObjectPermissionMixin
from wiki.permissions.object.enums import ObjectPermissionType, ObjectType
from wiki.permissions.object.repository import ObjectPermissionRepository
from wiki.permissions.object.schemas import (
    GeneralObjectPermissionInfo,
    GroupObjectPermissionInfo,
    IndividualObjectPermissionInfo,
    CreateGeneralObjectPermission,
    CreateGroupObjectPermission,
    CreateIndividualObjectPermission, UpdateBaseObjectPermission, UpdateGeneralObjectPermission
)
from wiki.permissions.object.utils import get_object_for_permission, get_db_permission_class
from wiki.user.repository import UserRepository
from wiki.user_group.repository import GroupRepository
from wiki.wiki_api_client.enums import ResponsibilityType


object_permission_router = APIRouter()


@object_permission_router.get(
    "/general/object_type/{object_type}/object_id/",
    response_model=list[GeneralObjectPermissionInfo],
    status_code=status.HTTP_200_OK,
    summary="Get all general permission by object type"
)
async def get_object_permissions_general(
        object_type: ObjectType,
        object_id: UUID,
        user: WikiUserHandlerData = Depends(BasePermission(responsibility=ResponsibilityType.VIEWER)),
        session: AsyncSession = Depends(get_db)
):
    permission_repository = ObjectPermissionRepository(session)
    permission_object = await get_object_for_permission(object_type, object_id, session)
    permissions = await permission_repository.get_permissions_for_object(
        permission_object,
        get_db_permission_class(ObjectPermissionType.GENERAL, object_type)
    )

    return [
        permission.get_permission_info() for permission in permissions
    ]


@object_permission_router.get(
    "/user/{user_id}/object_type/{object_type}/",
    response_model=list[IndividualObjectPermissionInfo],
    status_code=status.HTTP_200_OK,
    summary="Get all individual permission for user by object type"
)
async def get_object_permissions_for_user(
        user_id: UUID,
        object_type: ObjectType,
        user: WikiUserHandlerData = Depends(BasePermission(responsibility=ResponsibilityType.VIEWER)),
        session: AsyncSession = Depends(get_db)
):
    if user.wiki_api_client.responsibility == ResponsibilityType.ADMIN or user.id == user_id:
        permission_repository = ObjectPermissionRepository(session)
        user_repository = UserRepository(session)
        user_db = await user_repository.get_user_by_id(user_id)
        permissions = await permission_repository.get_permissions_for_user(
            user_db,
            get_db_permission_class(ObjectPermissionType.INDIVIDUAL, object_type)
        )

        return [
            permission.get_permission_info() for permission in permissions
        ]
    else:
        raise WikiException(
            message="You do not have access to these permissions as they do not belong to you",
            error_code=WikiErrorCode.OBJECT_PERMISSION_FORBIDDEN,
            http_status_code=status.HTTP_403_FORBIDDEN
        )


@object_permission_router.get(
    "/group/{group_id}/object_type/{object_type}/",
    response_model=list[GroupObjectPermissionInfo],
    status_code=status.HTTP_200_OK,
    summary="Get all permission from group by object type"
)
async def get_object_permissions_for_group(
        group_id: UUID,
        object_type: ObjectType,
        user: WikiUserHandlerData = Depends(BasePermission(responsibility=ResponsibilityType.VIEWER)),
        session: AsyncSession = Depends(get_db)
):
    group_repository = GroupRepository(session)
    group = await group_repository.get_group_by_id(group_id)
    user_repository = UserRepository(session)
    user_db = await user_repository.get_user_by_id(user.id)
    user_group = await group_repository.get_user_group(group, user_db)
    if user.wiki_api_client.responsibility == ResponsibilityType.ADMIN or user_group is not None:
        permission_repository = ObjectPermissionRepository(session)
        permissions = await permission_repository.get_permissions_for_group(
            group,
            get_db_permission_class(ObjectPermissionType.GROUP, object_type)
        )

        return [
            permission.get_permission_info() for permission in permissions
        ]
    else:
        raise WikiException(
            message="You do not have access to these permissions because you are not in the group",
            error_code=WikiErrorCode.OBJECT_PERMISSION_FORBIDDEN,
            http_status_code=status.HTTP_403_FORBIDDEN
        )


@object_permission_router.put(
    "/admin/permission_type/{permission_type}/object_type/{object_type}/{permission_id}",
    response_model=GeneralObjectPermissionInfo | GroupObjectPermissionInfo | IndividualObjectPermissionInfo,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Create object permission"
)
async def update_object_permission(
        permission_type: ObjectPermissionType,
        object_type: ObjectType,
        permission_id: UUID,
        update_permission: UpdateBaseObjectPermission | UpdateGeneralObjectPermission,
        user: WikiUserHandlerData = Depends(BasePermission(responsibility=ResponsibilityType.ADMIN)),
        session: AsyncSession = Depends(get_db)
):
    permission_repository = ObjectPermissionRepository(session)
    permission = await permission_repository.get_permission_by_id(
        get_db_permission_class(permission_type, object_type),
        permission_id
    )

    if permission_type == ObjectPermissionType.GENERAL and isinstance(update_permission, UpdateGeneralObjectPermission):
        permission = await permission_repository.update_general_permission(permission, update_permission)
    else:
        permission = await permission_repository.update_user_permission(permission, update_permission)

    return permission.get_permission_info()


@object_permission_router.post(
    "/admin/permission_type/{permission_type}/object_type/{object_type}/{object_id}",
    response_model=GeneralObjectPermissionInfo | GroupObjectPermissionInfo | IndividualObjectPermissionInfo,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Create object permission"
)
async def create_object_permission(
        permission_type: ObjectPermissionType,
        object_type: ObjectType,
        object_id: UUID,
        create_permission: CreateGeneralObjectPermission | CreateGroupObjectPermission | CreateIndividualObjectPermission,
        user: WikiUserHandlerData = Depends(BasePermission(responsibility=ResponsibilityType.ADMIN)),
        session: AsyncSession = Depends(get_db)
):
    permission_repository = ObjectPermissionRepository(session)
    permission_object = await get_object_for_permission(object_type, object_id, session)
    permission: BaseObjectPermissionMixin

    if permission_type == ObjectPermissionType.GENERAL and isinstance(create_permission, CreateGeneralObjectPermission):
        permission = await permission_repository.create_general_permission(create_permission, permission_object)
    elif permission_type == ObjectPermissionType.GROUP and isinstance(create_permission, CreateGroupObjectPermission):
        permission = await permission_repository.create_group_permission(create_permission, permission_object)
    elif permission_type == ObjectPermissionType.INDIVIDUAL and isinstance(create_permission, CreateIndividualObjectPermission):
        permission = await permission_repository.create_individual_permission(create_permission, permission_object)
    else:
        raise WikiException(
            message="Permission type data is incorrect",
            error_code=WikiErrorCode.OBJECT_TYPE_DATA_FOR_PERMISSION_INCORRECT,
            http_status_code=status.HTTP_409_CONFLICT
        )

    return permission.get_permission_info()
