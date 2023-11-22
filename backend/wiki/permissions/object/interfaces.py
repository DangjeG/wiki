from abc import abstractmethod
from uuid import UUID

from wiki.permissions.object.enums import ObjectPermissionMode
from wiki.permissions.object.general.models import GeneralObjectPermissionMixin
from wiki.permissions.object.group.models import GroupObjectPermissionMixin
from wiki.permissions.object.individual.models import IndividualObjectPermissionMixin
from wiki.wiki_api_client.enums import ResponsibilityType


class IGenObjectPermission:
    @abstractmethod
    def gen_general_object_permission(self,
                                      mode: ObjectPermissionMode,
                                      required_responsibility: ResponsibilityType) -> GeneralObjectPermissionMixin:
        pass

    @abstractmethod
    def gen_group_object_permission(self,
                                    mode: ObjectPermissionMode,
                                    group_id: UUID) -> GroupObjectPermissionMixin:
        pass

    @abstractmethod
    def gen_individual_object_permission(self,
                                         mode: ObjectPermissionMode,
                                         user_id: UUID) -> IndividualObjectPermissionMixin:
        pass
