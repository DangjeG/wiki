from abc import abstractmethod

from wiki.permissions.object.schemas import (
    CreateGeneralObjectPermission,
    CreateGroupObjectPermission,
    CreateIndividualObjectPermission, BaseObjectPermissionInfo
)
from wiki.wiki_workspace.block.schemas import BlockInfoResponse
from wiki.wiki_workspace.document.schemas import DocumentInfoResponse
from wiki.wiki_workspace.schemas import WorkspaceInfoResponse


class IGenObjectPermission:
    @abstractmethod
    def gen_general_object_permission(self,
                                      create_permission: CreateGeneralObjectPermission):
        pass

    @abstractmethod
    def gen_group_object_permission(self, create_permission: CreateGroupObjectPermission):
        pass

    @abstractmethod
    def gen_individual_object_permission(self, create_permission: CreateIndividualObjectPermission):
        pass


class IGetPermissionInfo:
    @abstractmethod
    def get_permission_info(self) -> BaseObjectPermissionInfo:
        pass
