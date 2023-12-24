from sqlalchemy import Column, ForeignKey, UniqueConstraint

from wiki.database.core import Base
from wiki.permissions.object.base import BaseObjectPermissionMixin
from wiki.permissions.object.schemas import GroupObjectPermissionInfo


class GroupObjectPermissionMixin(BaseObjectPermissionMixin):
    group_id = Column(ForeignKey("group.id"), nullable=False)

    # For each object there can be only one permission for each group
    __table_args__ = tuple(
        UniqueConstraint(
            "object_id",
            "group_id",
            name="group_object_permission_uc")
    )

    def get_permission_info(self) -> GroupObjectPermissionInfo:
        return GroupObjectPermissionInfo(
            id=self.id,
            mode=self.mode,
            object=self.object_id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            group_id=self.group_id
        )


class GroupWorkspacePermission(Base, GroupObjectPermissionMixin):
    object_id = Column(ForeignKey("workspace.id"), nullable=False)


class GroupDocumentPermission(Base, GroupObjectPermissionMixin):
    object_id = Column(ForeignKey("document.id"), nullable=False)


class GroupBlockPermission(Base, GroupObjectPermissionMixin):
    object_id = Column(ForeignKey("block.id"), nullable=False)
