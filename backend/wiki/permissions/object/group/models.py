from sqlalchemy import Column, ForeignKey

from wiki.database.core import Base
from wiki.permissions.object.base import BaseObjectPermissionMixin


class GroupObjectPermissionMixin(BaseObjectPermissionMixin):
    group_id = Column(ForeignKey("group.id"), nullable=False)


class GroupWorkspacePermission(Base, GroupObjectPermissionMixin):
    object_id = Column(ForeignKey("workspace.id"), nullable=False)


class GroupDocumentPermission(Base, GroupObjectPermissionMixin):
    object_id = Column(ForeignKey("document.id"), nullable=False)


class GroupBlockPermission(Base, GroupObjectPermissionMixin):
    object_id = Column(ForeignKey("block.id"), nullable=False)
