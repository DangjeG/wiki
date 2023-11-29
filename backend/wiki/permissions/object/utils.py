from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from wiki.common.exceptions import WikiException, WikiErrorCode
from wiki.permissions.object.enums import ObjectType, ObjectPermissionType
from wiki.permissions.object.general.models import (
    GeneralWorkspacePermission,
    GeneralDocumentPermission,
    GeneralBlockPermission
)
from wiki.permissions.object.group.models import (
    GroupWorkspacePermission,
    GroupDocumentPermission,
    GroupBlockPermission
)
from wiki.permissions.object.individual.models import (
    IndividualWorkspacePermission,
    IndividualDocumentPermission,
    IndividualBlockPermission
)
from wiki.wiki_workspace.block.repository import BlockRepository
from wiki.wiki_workspace.document.repository import DocumentRepository
from wiki.wiki_workspace.repository import WorkspaceRepository


async def get_object_for_permission(object_type: ObjectType, object_id: UUID, session: AsyncSession):
    match object_type:
        case ObjectType.WORKSPACE:
            repository = WorkspaceRepository(session)
            return await repository.get_workspace_by_id(object_id)
        case ObjectType.DOCUMENT:
            repository = DocumentRepository(session)
            return await repository.get_document_by_id(object_id)
        case ObjectType.BLOCK:
            repository = BlockRepository(session)
            return await repository.get_block_by_id(object_id)
        case _:
            raise WikiException(
                message="The type of object to permission is not available",
                error_code=WikiErrorCode.OBJECT_TYPE_FOR_PERMISSION_NOT_AVAILABLE,
                http_status_code=status.HTTP_400_BAD_REQUEST
            )


_permission_bd_classes = [GeneralWorkspacePermission, GeneralDocumentPermission, GeneralBlockPermission,
                          GroupWorkspacePermission, GroupDocumentPermission, GroupBlockPermission,
                          IndividualWorkspacePermission, IndividualDocumentPermission, IndividualBlockPermission]


def get_db_permission_class(permission_type: ObjectPermissionType, object_type: ObjectType):
    for item in _permission_bd_classes:
        if item.__name__ == f"{permission_type.value}{object_type.value}Permission":
            return item
