from uuid import UUID

from fastapi import APIRouter, Depends
from lakefs_client.client import LakeFSClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import Response

from wiki.common.schemas import WikiUserHandlerData
from wiki.database.deps import get_db
from wiki.database.utils import utcnow
from wiki.permissions.base import BasePermission
from wiki.wiki_api_client.enums import ResponsibilityType
from wiki.wiki_storage.deps import get_storage_client
from wiki.wiki_storage.services.versioning import VersioningWikiStorageService
from wiki.wiki_workspace.block.repository import BlockRepository
from wiki.wiki_workspace.document.export.utils import export_document_docx
from wiki.wiki_workspace.document.repository import DocumentRepository

document_export_router = APIRouter()


@document_export_router.post(
    "/export",
    response_class=Response,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Export published version document"
)
async def document_to_docx(
        document_id: UUID,
        session: AsyncSession = Depends(get_db),
        storage_client: LakeFSClient = Depends(get_storage_client),
        user: WikiUserHandlerData = Depends(BasePermission(responsibility=ResponsibilityType.VIEWER))
):
    document_repository: DocumentRepository = DocumentRepository(session)
    document = await document_repository.get_document_by_id(document_id, False)

    block_repository: BlockRepository = BlockRepository(session)

    list_blocks_document = await block_repository.get_all_block_with_permissions_by_document_id(user.id,
                                                                                                document_id,
                                                                                                document.current_published_version_commit_id)

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

    title = f"document-{document.title}-{utcnow()}.docx"
    res = export_document_docx(list_content_document, title)
    headers = {"Content-Disposition": f'attachment; filename="{title}"'}
    resp = Response(content=res, headers=headers, media_type='application/msword;charset="ISO-8859-1"')
    resp.charset = "ISO-8859-1"

    return resp
