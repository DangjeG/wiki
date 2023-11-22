from sqlalchemy import Column, String, ForeignKey

from wiki.database.core import Base
from wiki.permissions.object.base import BaseObjectPermissionMixin
from wiki.wiki_api_client.enums import ResponsibilityType


class GeneralObjectPermissionMixin(BaseObjectPermissionMixin):
    required_responsibility = Column(String, nullable=False, default=str(ResponsibilityType.VIEWER))


class GeneralWorkspacePermission(Base, GeneralObjectPermissionMixin):
    object_id = Column(ForeignKey("workspace.id"), nullable=False, unique=True)


class GeneralDocumentPermission(Base, GeneralObjectPermissionMixin):
    object_id = Column(ForeignKey("document.id"), nullable=False, unique=True)


class GeneralBlockPermission(Base, GeneralObjectPermissionMixin):
    object_id = Column(ForeignKey("block.id"), nullable=False, unique=True)
