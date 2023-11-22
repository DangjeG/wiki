from wiki.database.repository import BaseRepository
from wiki.database.utils import menage_db_commit_method, CommitMode
from wiki.permissions.object.enums import ObjectPermissionMode
from wiki.permissions.object.general.models import GeneralObjectPermissionMixin
from wiki.permissions.object.group.models import GroupObjectPermissionMixin
from wiki.permissions.object.individual.models import IndividualObjectPermissionMixin
from wiki.permissions.object.interfaces import IGenObjectPermission
from wiki.user.models import User
from wiki.user_group.models import Group
from wiki.wiki_api_client.enums import ResponsibilityType


class ObjectPermissionRepository(BaseRepository):
    @menage_db_commit_method(CommitMode.FLUSH)
    async def create_general_permission(self,
                                        mode: ObjectPermissionMode,
                                        required_responsibility: ResponsibilityType,
                                        permission_object: IGenObjectPermission) -> GeneralObjectPermissionMixin:
        new = permission_object.gen_general_object_permission(mode, required_responsibility)
        self.session.add(new)

        return new

    @menage_db_commit_method(CommitMode.FLUSH)
    async def create_group_permission(self,
                                      mode: ObjectPermissionMode,
                                      group: Group,
                                      permission_object: IGenObjectPermission) -> GroupObjectPermissionMixin:
        new = permission_object.gen_group_object_permission(mode, group.id)
        self.session.add(new)

        return new

    @menage_db_commit_method(CommitMode.FLUSH)
    async def create_individual_permission(self,
                                           mode: ObjectPermissionMode,
                                           user: User,
                                           permission_object: IGenObjectPermission) -> IndividualObjectPermissionMixin:
        new = permission_object.gen_individual_object_permission(mode, user.id)
        self.session.add(new)

        return new
