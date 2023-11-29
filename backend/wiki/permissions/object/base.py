from abc import abstractmethod

from sqlalchemy import Column, Uuid, String
from uuid_extensions import uuid7

from wiki.common.models import TimeStampMixin
from wiki.permissions.object.enums import ObjectPermissionMode
from wiki.permissions.object.interfaces import IGetPermissionInfo
from wiki.permissions.object.schemas import BaseObjectPermissionInfo
from wiki.wiki_workspace.block.schemas import BlockInfoResponse
from wiki.wiki_workspace.document.schemas import DocumentInfoResponse
from wiki.wiki_workspace.schemas import WorkspaceInfoResponse


class BaseObjectPermissionMixin(TimeStampMixin, IGetPermissionInfo):
    id = Column(Uuid, default=uuid7, primary_key=True, nullable=False)
    mode = Column(String, nullable=False, default=str(ObjectPermissionMode.HIDDEN_INACCESSIBLE))
    object_id: Column

    @abstractmethod
    def get_permission_info(self) -> BaseObjectPermissionInfo:
        pass
