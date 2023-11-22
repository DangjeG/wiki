from uuid import UUID

from sqlalchemy import Column, Uuid, String, ForeignKey
from uuid_extensions import uuid7

from wiki.common.models import EnabledDeletedMixin
from wiki.database.core import Base
from wiki.permissions.object.enums import ObjectPermissionMode
from wiki.permissions.object.general.models import GeneralWorkspacePermission, GeneralObjectPermissionMixin
from wiki.permissions.object.group.models import GroupObjectPermissionMixin, GroupWorkspacePermission
from wiki.permissions.object.individual.models import IndividualObjectPermissionMixin, IndividualWorkspacePermission
from wiki.permissions.object.interfaces import IGenObjectPermission
from wiki.wiki_api_client.enums import ResponsibilityType


class Workspace(Base, EnabledDeletedMixin, IGenObjectPermission):
    id = Column(Uuid, default=uuid7, primary_key=True, nullable=False)

    title = Column(String, nullable=False)

    owner_user_id = Column(ForeignKey("user.id"), nullable=False)

    def __init__(self,
                 title: str,
                 owner_user_id: UUID):
        self.title = title
        self.owner_user_id = owner_user_id

    def gen_general_object_permission(self,
                                      mode: ObjectPermissionMode,
                                      required_responsibility: ResponsibilityType) -> GeneralObjectPermissionMixin:
        return GeneralWorkspacePermission(
            mode=str(mode),
            required_responsibility=str(required_responsibility),
            object_id=self.id
        )

    def gen_group_object_permission(self,
                                    mode: ObjectPermissionMode,
                                    group_id: UUID) -> GroupObjectPermissionMixin:
        return GroupWorkspacePermission(
            mode=str(mode),
            group_id=group_id,
            object_id=self.id
        )

    def gen_individual_object_permission(self,
                                         mode: ObjectPermissionMode,
                                         user_id: UUID) -> IndividualObjectPermissionMixin:
        return IndividualWorkspacePermission(
            mode=str(mode),
            user_id=user_id,
            object_id=self.id
        )
