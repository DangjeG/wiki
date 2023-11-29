from uuid import UUID

from sqlalchemy import Column, String, ForeignKey, UniqueConstraint

from wiki.database.core import Base
from wiki.permissions.object.base import BaseObjectPermissionMixin
from wiki.permissions.object.schemas import GeneralObjectPermissionInfo
from wiki.wiki_api_client.enums import ResponsibilityType
from wiki.wiki_workspace.block.schemas import BlockInfoResponse
from wiki.wiki_workspace.document.schemas import DocumentInfoResponse
from wiki.wiki_workspace.schemas import WorkspaceInfoResponse


class GeneralObjectPermissionMixin(BaseObjectPermissionMixin):
    required_responsibility = Column(String, nullable=False, default=str(ResponsibilityType.VIEWER))

    # There can only be one permission for each facility for each level of responsibility
    __table_args__ = tuple(
        UniqueConstraint(
            "object_id",
            "required_responsibility",
            name="general_object_permission_uc")
    )

    def get_permission_info(self, **kwargs) -> GeneralObjectPermissionInfo:
        return GeneralObjectPermissionInfo(
            id=self.id,
            mode=self.mode,
            object_id=self.object_id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            required_responsibility=self.required_responsibility
        )


class GeneralWorkspacePermission(Base, GeneralObjectPermissionMixin):
    object_id = Column(ForeignKey("workspace.id"), nullable=False, unique=True)


class GeneralDocumentPermission(Base, GeneralObjectPermissionMixin):
    object_id = Column(ForeignKey("document.id"), nullable=False, unique=True)


class GeneralBlockPermission(Base, GeneralObjectPermissionMixin):
    object_id = Column(ForeignKey("block.id"), nullable=False, unique=True)
