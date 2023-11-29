from wiki.wiki_storage.services.base import BaseWikiStorageService
from wiki.wiki_workspace.block.model import TypeBlock
from wiki.wiki_workspace.block.repository import BlockRepository
from wiki.wiki_workspace.block.schemas import BlockDataResponse
from wiki.wiki_workspace.document.repository import DocumentRepository
from wiki.wiki_workspace.repository import WorkspaceRepository


async def get_block_data_by_id(session, block_id, storage_client, version_commit_id):
    block_repository: BlockRepository = BlockRepository(session)

    block = await block_repository.get_block_by_id(block_id)
    document_repository: DocumentRepository = DocumentRepository(session)
    document = await document_repository.get_document_by_id(block.document_id)
    document_ids = await document_repository.get_list_ids_of_document_hierarchy(document)
    workspace_repository: WorkspaceRepository = WorkspaceRepository(session)
    workspace = await workspace_repository.get_workspace_by_id(document.workspace_id)

    storage_service: BaseWikiStorageService = BaseWikiStorageService(storage_client)

    return BlockDataResponse(
        id=block.id,
        document_id=block.document_id,
        position=block.position,
        type_block=block.type_block,
        content=storage_service.get_content_document_block_in_workspace_storage(document.workspace_id,
                                                                                document_ids,
                                                                                block.id,
                                                                                version_commit_id),
        created_at=block.created_at
    )


async def get_data_blocks(session,
                          document_id,
                          version_commit_id,
                          storage_client):
    block_repository: BlockRepository = BlockRepository(session)

    blocks = await block_repository.get_all_block_by_document_id(document_id=document_id)
    document_repository: DocumentRepository = DocumentRepository(session)
    document = await document_repository.get_document_by_id(document_id)
    document_ids = await document_repository.get_list_ids_of_document_hierarchy(document)
    workspace_repository: WorkspaceRepository = WorkspaceRepository(session)
    workspace = await workspace_repository.get_workspace_by_id(document.workspace_id)

    storage_service: BaseWikiStorageService = BaseWikiStorageService(storage_client)
    result_blocks: list[BlockDataResponse] = []
    for block in blocks:
        append_block = BlockDataResponse(
            id=block.id,
            document_id=block.document_id,
            position=block.position,
            type_block=block.type_block,
            content=storage_service.get_content_document_block_in_workspace_storage(document.workspace_id,
                                                                                    document_ids,
                                                                                    block.id,
                                                                                    version_commit_id),
            created_at=block.created_at
        )
        result_blocks.append(append_block)

    return result_blocks
