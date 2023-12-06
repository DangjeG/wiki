from sqlalchemy.ext.asyncio import AsyncSession

from wiki.permissions.object.enums import ObjectPermissionType, ObjectType
from wiki.permissions.object.repository import ObjectPermissionRepository
from wiki.permissions.object.schemas import (
    CreateGeneralObjectPermission,
    CreateGroupObjectPermission,
    CreateIndividualObjectPermission
)
from wiki.permissions.object.utils import get_db_permission_class
from wiki.wiki_workspace.block.model import Block
from wiki.wiki_workspace.document.model import Document
from wiki.wiki_workspace.model import Workspace


class PermissionTransporter:
    """
    Class to migrate all permissions for newly created elements
    """

    session: AsyncSession
    permission_repository: ObjectPermissionRepository

    def __init__(self, session):
        self.session = session
        self.permission_repository = ObjectPermissionRepository(session)

    async def _transfer_general_permission(self,
                                           object_permission,
                                           transmitting_object_permission,
                                           transmitting_object_type: ObjectType):
        general_permissions = await self.permission_repository.get_permissions_for_object(
            transmitting_object_permission,
            get_db_permission_class(ObjectPermissionType.GENERAL, transmitting_object_type)
        )
        for permission in general_permissions:
            await self.permission_repository.create_general_permission(CreateGeneralObjectPermission(
                mode=permission.mode,
                required_responsibility=permission.required_responsibility),
                object_permission
            )

    async def _transfer_group_permission(self,
                                         object_permission,
                                         transmitting_object_permission,
                                         transmitting_object_type: ObjectType):
        group_permissions = await self.permission_repository.get_permissions_for_object(
            transmitting_object_permission,
            get_db_permission_class(ObjectPermissionType.GROUP, transmitting_object_type)
        )
        for permission in group_permissions:
            await self.permission_repository.create_group_permission(
                CreateGroupObjectPermission(
                    mode=permission.mode,
                    group_id=permission.group_id
                ),
                object_permission
            )

    async def _transfer_individual_permission(self,
                                              object_permission,
                                              transmitting_object_permission,
                                              transmitting_object_type: ObjectType):
        individual_permissions = await self.permission_repository.get_permissions_for_object(
            transmitting_object_permission,
            get_db_permission_class(ObjectPermissionType.INDIVIDUAL, transmitting_object_type)
        )
        for permission in individual_permissions:
            await self.permission_repository.create_group_permission(
                CreateIndividualObjectPermission(
                    mode=permission.mode,
                    user_id=permission.user_id
                ),
                object_permission
            )

    async def _transfer_all_permissions(self,
                                        object_permission,
                                        transmitting_object_permission,
                                        transmitting_object_type: ObjectType):
        await self._transfer_general_permission(object_permission, transmitting_object_permission, transmitting_object_type)
        await self._transfer_group_permission(object_permission, transmitting_object_permission, transmitting_object_type)
        await self._transfer_individual_permission(object_permission, transmitting_object_permission, transmitting_object_type)

    async def transfer_to_document(self, document: Document, workspace: Workspace):
        await self._transfer_all_permissions(document, workspace, ObjectType.WORKSPACE)

    async def transfer_to_block(self, block: Block, document: Document):
        await self._transfer_all_permissions(block, document, ObjectType.DOCUMENT)
