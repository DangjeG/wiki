from io import StringIO
from uuid import UUID

from fastapi import APIRouter, Depends
from lakefs_client.client import LakeFSClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from wiki.common.schemas import BaseResponse
from wiki.database.deps import get_db
from wiki.wiki_storage.deps import get_storage_client
from wiki.wiki_storage.services.base import BaseWikiStorageService
from wiki.wiki_storage.utils import get_unique_names_parents_documents
from wiki.wiki_workspace.block.repository import BlockRepository
from wiki.wiki_workspace.block.schemas import CreateBlock, BlockDataResponse
from wiki.wiki_workspace.document.repository import DocumentRepository
from wiki.wiki_workspace.repository import WorkspaceRepository

block_router = APIRouter()


@block_router.post(
    "/",
    response_model=BaseResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Create block."
)
async def create_block(
        new_block: CreateBlock,
        session: AsyncSession = Depends(get_db),
        storage_client: LakeFSClient = Depends(get_storage_client)
):
    document_repository: DocumentRepository = DocumentRepository(session)
    document = await document_repository.get_document_by_id(new_block.document_id)
    unique_workspace_name = document.workspace_id

    unique_names_parents_documents = await  get_unique_names_parents_documents(document, document_repository)

    block_repository: BlockRepository = BlockRepository(session)
    block = await block_repository.create_block(new_block)

    storage_service: BaseWikiStorageService = BaseWikiStorageService(storage_client)
    content_base = StringIO("")
    storage_service.upload_document_block_in_workspace_storage(content=content_base,
                                                               unique_workspace_name=unique_workspace_name,
                                                               unique_names_parents_documents=unique_names_parents_documents,
                                                               unique_block_name=block.id)

    return BlockDataResponse(
        id=block.id,
        document_id=document.id,
        type_block=new_block.type_block,
        content=content_base.getvalue()
    )


@block_router.get(
    "/",
    response_model=list[BlockDataResponse],
    status_code=status.HTTP_202_ACCEPTED,
    summary="Get all block by id document."
)
async def get_blocks(document_id: UUID,
                     session: AsyncSession = Depends(get_db),
                     storage_client: LakeFSClient = Depends(get_storage_client)):
    block_repository: BlockRepository = BlockRepository(session)

    blocks = await block_repository.get_all_block_by_document_id(document_id=document_id)
    document_repository: DocumentRepository = DocumentRepository(session)
    document = await document_repository.get_document_by_id(document_id)
    unique_names_parents_documents = await get_unique_names_parents_documents(document, document_repository)
    workspace_repository: WorkspaceRepository = WorkspaceRepository(session)
    workspace = workspace_repository.get_workspace_by_id(document.workspace_id)

    storage_service: BaseWikiStorageService = BaseWikiStorageService(storage_client)
    result_blocks: list[BlockDataResponse] = []
    for block in blocks:

        append_block = BlockDataResponse(
            id=block.id,
            document_id=block.document_id,
            type_block=block.type_block,
            content=storage_service.get_content_document_block_in_workspace_storage(document.workspace_id,
                                                                                    unique_names_parents_documents,
                                                                                    block.id)
        )
        result_blocks.append(append_block)

    return result_blocks
