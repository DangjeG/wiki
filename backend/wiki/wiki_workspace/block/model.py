from uuid import UUID

from sqlalchemy import Column, Uuid, ForeignKey, String, Integer
from uuid_extensions import uuid7

from wiki.common.enums import WikiBaseEnum
from wiki.common.models import EnabledDeletedMixin
from wiki.database.core import Base
from wiki.permissions.object.enums import ObjectPermissionMode
from wiki.permissions.object.general.models import GeneralObjectPermissionMixin, GeneralBlockPermission
from wiki.permissions.object.group.models import GroupObjectPermissionMixin, GroupBlockPermission
from wiki.permissions.object.individual.models import IndividualObjectPermissionMixin, IndividualBlockPermission
from wiki.permissions.object.interfaces import IGenObjectPermission
from wiki.wiki_api_client.enums import ResponsibilityType


class TypeBlock(WikiBaseEnum):
    IMG = "IMG"
    TEXT = "TEXT"
    FILE = "FILE"
    # VIDEO = "VIDEO"


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

    def gen_general_object_permission(self,
                                      mode: ObjectPermissionMode,
                                      required_responsibility: ResponsibilityType) -> GeneralObjectPermissionMixin:
        return GeneralBlockPermission(
            mode=str(mode),
            required_responsibility=str(required_responsibility),
            object_id=self.id
        )

    def gen_group_object_permission(self,
                                    mode: ObjectPermissionMode,
                                    group_id: UUID) -> GroupObjectPermissionMixin:
        return GroupBlockPermission(
            mode=str(mode),
            group_id=group_id,
            object_id=self.id
        )

    def gen_individual_object_permission(self,
                                         mode: ObjectPermissionMode,
                                         user_id: UUID) -> IndividualObjectPermissionMixin:
        return IndividualBlockPermission(
            mode=str(mode),
            user_id=user_id,
            object_id=self.id
        )
