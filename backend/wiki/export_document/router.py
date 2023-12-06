from uuid import UUID

from fastapi import APIRouter, Depends
from lakefs_client.client import LakeFSClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import StreamingResponse

from wiki.common.schemas import WikiUserHandlerData
from wiki.database.deps import get_db
from wiki.export_document.utils import export_document
from wiki.permissions.base import BasePermission
from wiki.wiki_api_client.enums import ResponsibilityType
from wiki.wiki_storage.deps import get_storage_client
from wiki.wiki_storage.services.versioning import VersioningWikiStorageService
from wiki.wiki_workspace.block.repository import BlockRepository
from wiki.wiki_workspace.document.repository import DocumentRepository

export_document_router = APIRouter()

@export_document_router.get(
    "/",
    response_model=None,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Export Docx"
)
async def download_docx(
        document_id: UUID,
        session: AsyncSession = Depends(get_db),
        storage_client: LakeFSClient = Depends(get_storage_client),
        user: WikiUserHandlerData = Depends(BasePermission(responsibility=ResponsibilityType.VIEWER))
):
    document_repository: DocumentRepository = DocumentRepository(session)
    document = await document_repository.get_document_by_id(document_id, False)

    block_repository: BlockRepository = BlockRepository(session)

    list_blocks_document = await block_repository.get_all_block_by_document_id(document_id)

    storage_service: VersioningWikiStorageService = VersioningWikiStorageService(storage_client)

    list_content_document = []

    for block in list_blocks_document:

        document_ids = await document_repository.get_list_ids_of_document_hierarchy(document)

        content = storage_service.get_content_document_block_in_workspace_storage(
            workspace_id=document.workspace_id,
            document_ids=document_ids,
            block_id=block.id,
            version_commit_id=document.current_published_version_commit_id
        )
        list_content_document.append(content)

    file_name = "export"

    bytes = await export_document(
        file_name=file_name,
        list_document_content=list_content_document
    )

    headers = {"Content-Disposition": f'attachment; filename="{file_name}.docx"'}

    return StreamingResponse(content=bytes.read(), headers=headers, media_type='application/msword')
