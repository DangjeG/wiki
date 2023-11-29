from uuid import UUID

from sqlalchemy import select, and_
from sqlalchemy.exc import IntegrityError
from starlette import status

from wiki.common.exceptions import WikiException, WikiErrorCode
from wiki.database.repository import BaseRepository
from wiki.database.utils import (
    menage_db_commit_method,
    CommitMode,
    menage_db_not_found_result_method,
    NotFoundResultMode, manage_db_exception_method
)
from wiki.permissions.object.base import BaseObjectPermissionMixin
from wiki.permissions.object.general.models import GeneralObjectPermissionMixin
from wiki.permissions.object.group.models import GroupObjectPermissionMixin
from wiki.permissions.object.individual.models import IndividualObjectPermissionMixin
from wiki.permissions.object.interfaces import IGenObjectPermission
from wiki.permissions.object.schemas import (
    CreateGeneralObjectPermission,
    CreateGroupObjectPermission,
    CreateIndividualObjectPermission,
    UpdateGeneralObjectPermission, UpdateBaseObjectPermission
)
from wiki.user.models import User
from wiki.user_group.models import Group


class ObjectPermissionRepository(BaseRepository):
    _object_permission_not_found = WikiException(
        message="Object permission not found.",
        error_code=WikiErrorCode.OBJECT_PERMISSION_NOT_FOUND,
        http_status_code=status.HTTP_404_NOT_FOUND
    )
    _object_permission_already_exist = WikiException(
        message="This object permission already exists",
        error_code=WikiErrorCode.OBJECT_PERMISSION_ALREADY_EXIST,
        http_status_code=status.HTTP_409_CONFLICT
    )

    @menage_db_not_found_result_method(NotFoundResultMode.EXCEPTION, ex=_object_permission_not_found)
    async def get_permission_by_id(self,
                                   permission_class: type[BaseObjectPermissionMixin],
                                   permission_id: UUID):
        return await self.session.get(permission_class, permission_id)

    async def get_all_permissions(self, permission_class: type[BaseObjectPermissionMixin]):
        return (await self.session.execute(select(permission_class))).scalars().all()

    async def get_permissions_for_user(self,
                                       user: User,
                                       user_permission_class: type[IndividualObjectPermissionMixin],
                                       *whereclause):
        st = select(user_permission_class).where(and_(user_permission_class.user_id == user.id, *whereclause))
        return (await self.session.execute(st)).scalars().all()

    async def get_permissions_for_group(self,
                                        group: Group,
                                        group_permission_class: type[GroupObjectPermissionMixin],
                                        *whereclause):
        st = select(group_permission_class).where(and_(group_permission_class.group_id == group.id, *whereclause))
        return (await self.session.execute(st)).scalars().all()

    async def get_permissions_for_object(self,
                                         object_permission,
                                         permission_class: type[BaseObjectPermissionMixin],
                                         *whereclause):
        st = select(permission_class).where(and_(permission_class.object_id == object_permission.id, *whereclause))
        return (await self.session.execute(st)).scalars().all()

    # @menage_db_not_found_result_method(NotFoundResultMode.EXCEPTION, ex=_object_permission_not_found)
    # async def get_permission_object_for_user(self,
    #                                          object_permission,
    #                                          user: User,
    #                                          user_permission_class: type[IndividualObjectPermissionMixin]):
    #     st = select(user_permission_class).where(and_(
    #         user_permission_class.user_id == user.id,
    #         user_permission_class.object_id == object_permission.id
    #     ))
    #     return (await self.session.execute(st)).scalar()
    #
    # @menage_db_not_found_result_method(NotFoundResultMode.EXCEPTION, ex=_object_permission_not_found)
    # async def get_permission_object_for_group(self,
    #                                           object_permission,
    #                                           group: Group,
    #                                           group_permission_class: type[GroupObjectPermissionMixin]):
    #     st = select(group_permission_class).where(and_(
    #         group_permission_class.group_id == group.id,
    #         group_permission_class.object_id == object_permission.id
    #     ))
    #     return (await self.session.execute(st)).scalar()

    # async def get_general_wp_permission_by_id(self, permission_id: UUID) -> GeneralWorkspacePermission:
    #     return await self.get_permission_by_id(GeneralWorkspacePermission, permission_id)
    #
    # async def get_general_doc_permission_by_id(self, permission_id: UUID) -> GeneralDocumentPermission:
    #     return await self.get_permission_by_id(GeneralDocumentPermission, permission_id)
    #
    # async def get_general_block_permission_by_id(self, permission_id: UUID) -> GeneralBlockPermission:
    #     return await self.get_permission_by_id(GeneralBlockPermission, permission_id)
    #
    # async def get_group_wp_permission_by_id(self, permission_id: UUID) -> GroupWorkspacePermission:
    #     return await self.get_permission_by_id(GroupWorkspacePermission, permission_id)
    #
    # async def get_group_doc_permission_by_id(self, permission_id: UUID) -> GroupDocumentPermission:
    #     return await self.get_permission_by_id(GroupDocumentPermission, permission_id)
    #
    # async def get_group_block_permission_by_id(self, permission_id: UUID) -> GroupBlockPermission:
    #     return await self.get_permission_by_id(GroupBlockPermission, permission_id)
    #
    # async def get_individual_wp_permission_by_id(self, permission_id: UUID) -> IndividualWorkspacePermission:
    #     return await self.get_permission_by_id(IndividualWorkspacePermission, permission_id)
    #
    # async def get_individual_doc_permission_by_id(self, permission_id: UUID) -> IndividualDocumentPermission:
    #     return await self.get_permission_by_id(IndividualDocumentPermission, permission_id)
    #
    # async def get_individual_block_permission_by_id(self, permission_id: UUID) -> IndividualBlockPermission:
    #     return await self.get_permission_by_id(IndividualBlockPermission, permission_id)

    @manage_db_exception_method(IntegrityError, _object_permission_already_exist)
    @menage_db_commit_method(CommitMode.FLUSH)
    async def create_general_permission(self,
                                        create_permission: CreateGeneralObjectPermission,
                                        permission_object: IGenObjectPermission) -> GeneralObjectPermissionMixin:
        new = permission_object.gen_general_object_permission(create_permission)
        self.session.add(new)

        return new

    @manage_db_exception_method(IntegrityError, _object_permission_already_exist)
    @menage_db_commit_method(CommitMode.FLUSH)
    async def update_general_permission(self,
                                        permission: GeneralObjectPermissionMixin,
                                        update_permission: UpdateGeneralObjectPermission):
        if update_permission.mode is not None:
            permission.mode = str(update_permission.mode)
        if update_permission.required_responsibility is not None:
            permission.required_responsibility = str(update_permission.required_responsibility)
        self.session.add(permission)

        return permission

    @manage_db_exception_method(IntegrityError, _object_permission_already_exist)
    @menage_db_commit_method(CommitMode.FLUSH)
    async def create_group_permission(self,
                                      create_permission: CreateGroupObjectPermission,
                                      permission_object: IGenObjectPermission) -> GroupObjectPermissionMixin:
        new = permission_object.gen_group_object_permission(create_permission)
        self.session.add(new)

        return new

    @manage_db_exception_method(IntegrityError, _object_permission_already_exist)
    @menage_db_commit_method(CommitMode.FLUSH)
    async def create_individual_permission(self,
                                           create_permission: CreateIndividualObjectPermission,
                                           permission_object: IGenObjectPermission) -> IndividualObjectPermissionMixin:
        new = permission_object.gen_individual_object_permission(create_permission)
        self.session.add(new)

        return new

    @menage_db_commit_method(CommitMode.FLUSH)
    async def update_user_permission(self,
                                     permission: GroupObjectPermissionMixin | IndividualObjectPermissionMixin,
                                     update_permission: UpdateBaseObjectPermission):
        if update_permission.mode is not None:
            permission.mode = str(update_permission.mode)
        self.session.add(permission)

        return permission
