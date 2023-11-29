from uuid import UUID

from sqlalchemy import Column, Uuid, ForeignKey, String, Integer
from uuid_extensions import uuid7

from wiki.common.models import EnabledDeletedMixin
from wiki.database.core import Base
from wiki.permissions.object.general.models import GeneralObjectPermissionMixin, GeneralBlockPermission
from wiki.permissions.object.group.models import GroupObjectPermissionMixin, GroupBlockPermission
from wiki.permissions.object.individual.models import IndividualObjectPermissionMixin, IndividualBlockPermission
from wiki.permissions.object.interfaces import IGenObjectPermission

from wiki.permissions.object.schemas import (
    CreateGeneralObjectPermission,
    CreateGroupObjectPermission,
    CreateIndividualObjectPermission
)
from wiki.wiki_workspace.block.enums import TypeBlock


class Block(Base, EnabledDeletedMixin, IGenObjectPermission):
    id = Column(Uuid, default=uuid7, primary_key=True, nullable=False)

    type_block = Column(String, nullable=False, default=str(TypeBlock.TEXT))
    position = Column(Integer, nullable=False)

    document_id = Column(ForeignKey("document.id"), nullable=False)

    def __init__(self,
                 document_id: UUID,
                 position: int,
                 type_block: TypeBlock):
        self.document_id = document_id
        self.position = position
        self.type_block = str(type_block)

    def gen_general_object_permission(self, create_permission: CreateGeneralObjectPermission) -> GeneralObjectPermissionMixin:
        return GeneralBlockPermission(
            mode=str(create_permission.mode),
            required_responsibility=str(create_permission.required_responsibility),
            object_id=self.id
        )

    def gen_group_object_permission(self, create_permission: CreateGroupObjectPermission) -> GroupObjectPermissionMixin:
        return GroupBlockPermission(
            mode=str(create_permission.mode),
            group_id=create_permission.group_id,
            object_id=self.id
        )

    def gen_individual_object_permission(self, create_permission: CreateIndividualObjectPermission) -> IndividualObjectPermissionMixin:
        return IndividualBlockPermission(
            mode=str(create_permission.mode),
            user_id=create_permission.user_id,
            object_id=self.id
        )
