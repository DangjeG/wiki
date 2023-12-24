from uuid import UUID

from sqlalchemy import Column, Uuid, String, ForeignKey
from uuid_extensions import uuid7

from wiki.common.models import EnabledDeletedMixin
from wiki.database.core import Base
from wiki.permissions.object.general.models import GeneralWorkspacePermission, GeneralObjectPermissionMixin
from wiki.permissions.object.group.models import GroupObjectPermissionMixin, GroupWorkspacePermission
from wiki.permissions.object.individual.models import IndividualObjectPermissionMixin, IndividualWorkspacePermission
from wiki.permissions.object.interfaces import IGenObjectPermission
from wiki.permissions.object.schemas import (
    CreateGeneralObjectPermission,
    CreateGroupObjectPermission,
    CreateIndividualObjectPermission
)


class Workspace(Base, EnabledDeletedMixin, IGenObjectPermission):
    id = Column(Uuid, default=uuid7, primary_key=True, nullable=False)

    title = Column(String, nullable=False)

    owner_user_id = Column(ForeignKey("user.id"), nullable=False)

    def __init__(self,
                 title: str,
                 owner_user_id: UUID):
        self.title = title
        self.owner_user_id = owner_user_id

    def gen_general_object_permission(self, create_permission: CreateGeneralObjectPermission) -> GeneralObjectPermissionMixin:
        return GeneralWorkspacePermission(
            mode=str(create_permission.mode),
            required_responsibility=str(create_permission.required_responsibility),
            object_id=self.id
        )

    def gen_group_object_permission(self, create_permission: CreateGroupObjectPermission) -> GroupObjectPermissionMixin:
        return GroupWorkspacePermission(
            mode=str(create_permission.mode),
            group_id=create_permission.group_id,
            object_id=self.id
        )

    def gen_individual_object_permission(self, create_permission: CreateIndividualObjectPermission) -> IndividualObjectPermissionMixin:
        return IndividualWorkspacePermission(
            mode=str(create_permission.mode),
            user_id=create_permission.user_id,
            object_id=self.id
        )
