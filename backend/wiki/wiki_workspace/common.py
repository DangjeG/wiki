from wiki.permissions.object.enums import ObjectPermissionMode
from wiki.permissions.object.utils import get_permission_mode_by_responsibility
from wiki.wiki_api_client.enums import ResponsibilityType
from wiki.wiki_storage.services.base import BaseWikiStorageService
from wiki.wiki_workspace.block.enums import TypeBlock
from wiki.wiki_workspace.block.repository import BlockRepository
from wiki.wiki_workspace.block.schemas import BlockDataResponse, WikiLinkSchema
from wiki.wiki_workspace.document.repository import DocumentRepository
from wiki.wiki_workspace.repository import WorkspaceRepository


async def get_block_data_by_id(session, user, block_id, storage_client, version_commit_id):
    block_repository: BlockRepository = BlockRepository(session)

    block = await block_repository.get_block_with_permission_by_id(user.id, block_id)

    if (user.wiki_api_client.responsibility == ResponsibilityType.ADMIN or
            ObjectPermissionMode(block.permission_mode) > ObjectPermissionMode.HIDDEN_INACCESSIBLE):
        document_repository: DocumentRepository = DocumentRepository(session)
        document = await document_repository.get_document_by_id(block.document_id)
        document_ids = await document_repository.get_list_ids_of_document_hierarchy(document)
        workspace_repository: WorkspaceRepository = WorkspaceRepository(session)
        workspace = await workspace_repository.get_workspace_by_id(document.workspace_id)

        content = str(ObjectPermissionMode.INACCESSIBLE)
        if (user.wiki_api_client.responsibility == ResponsibilityType.ADMIN or
                ObjectPermissionMode(block.permission_mode) > ObjectPermissionMode.INACCESSIBLE):
            storage_service: BaseWikiStorageService = BaseWikiStorageService(storage_client)
            content = storage_service.get_content_document_block_in_workspace_storage(document.workspace_id,
                                                                                      document_ids,
                                                                                      block.id,
                                                                                      version_commit_id)
            if TypeBlock(block.type_block) == TypeBlock.WIKI_LINK:
                content = WikiLinkSchema.get_from_content_string(content)

        return BlockDataResponse(
            id=block.id,
            document_id=block.document_id,
            position=block.position,
            type_block=block.type_block,
            content=content,
            created_at=block.created_at,
            permission_mode=get_permission_mode_by_responsibility(
                block.permission_mode,
                user.wiki_api_client.responsibility
            )
        )
    else:
        raise block_repository.block_not_found_exception


async def get_data_blocks(session,
                          user,
                          document_id,
                          version_commit_id,
                          storage_client):
    block_repository: BlockRepository = BlockRepository(session)

    blocks = await block_repository.get_all_block_with_permissions_by_document_id(user.id, document_id)
    document_repository: DocumentRepository = DocumentRepository(session)
    document = await document_repository.get_document_by_id(document_id)
    document_ids = await document_repository.get_list_ids_of_document_hierarchy(document)
    workspace_repository: WorkspaceRepository = WorkspaceRepository(session)
    workspace = await workspace_repository.get_workspace_by_id(document.workspace_id)

    storage_service: BaseWikiStorageService = BaseWikiStorageService(storage_client)
    result_blocks: list[BlockDataResponse] = []
    for block in blocks:
        if (user.wiki_api_client.responsibility == ResponsibilityType.ADMIN or
                ObjectPermissionMode(block.permission_mode) > ObjectPermissionMode.HIDDEN_INACCESSIBLE):
            content = str(ObjectPermissionMode.INACCESSIBLE)
            if (user.wiki_api_client.responsibility == ResponsibilityType.ADMIN or
                    ObjectPermissionMode(block.permission_mode) > ObjectPermissionMode.INACCESSIBLE):
                content = storage_service.get_content_document_block_in_workspace_storage(document.workspace_id,
                                                                                          document_ids,
                                                                                          block.id,
                                                                                          version_commit_id)
                if TypeBlock(block.type_block) == TypeBlock.WIKI_LINK:
                    content = WikiLinkSchema.get_from_content_string(content)

            append_block = BlockDataResponse(
                id=block.id,
                document_id=block.document_id,
                position=block.position,
                type_block=block.type_block,
                content=content,
                created_at=block.created_at,
                permission_mode=get_permission_mode_by_responsibility(
                    block.permission_mode,
                    user.wiki_api_client.responsibility
                )
            )
            result_blocks.append(append_block)

    return result_blocks
