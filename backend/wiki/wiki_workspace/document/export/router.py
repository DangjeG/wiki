from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends
from lakefs_client.client import LakeFSClient
from pydantic import constr
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import Response
from yadisk_async import YaDisk

from wiki.asset.repository import AssetRepository
from wiki.assets_storage.deps import get_ya_disk_session_storage
from wiki.assets_storage.services.yadisk import YaDiskAssetsStorage
from wiki.common.schemas import WikiUserHandlerData
from wiki.database.deps import get_db
from wiki.database.utils import utcnow
from wiki.permissions.base import BasePermission
from wiki.permissions.object.enums import ObjectPermissionMode
from wiki.wiki_api_client.enums import ResponsibilityType
from wiki.wiki_storage.deps import get_storage_client
from wiki.wiki_storage.services.versioning import VersioningWikiStorageService
from wiki.wiki_workspace.block.enums import TypeBlock
from wiki.wiki_workspace.block.repository import BlockRepository
from wiki.wiki_workspace.document.export.deps import get_converters, DocumentConverters
from wiki.wiki_workspace.document.export.enums import DocumentExportType
from wiki.wiki_workspace.document.export.templates.html import (
    get_html_base_img_teg,
    get_html_base_file,
    get_html_frame
)
from wiki.wiki_workspace.document.export.utils import export_document_docx
from wiki.wiki_workspace.document.repository import DocumentRepository

document_export_router = APIRouter()


@document_export_router.post(
    "/export",
    response_class=Response,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Export document"
)
async def export_document(
        document_id: UUID,
        export_type: DocumentExportType = DocumentExportType.DOCX,
        version_commit_id: Optional[constr(min_length=64, max_length=64)] = None,
        session: AsyncSession = Depends(get_db),
        converters: DocumentConverters = Depends(get_converters),
        storage_client: LakeFSClient = Depends(get_storage_client),
        ya_disk: YaDisk = Depends(get_ya_disk_session_storage),
        user: WikiUserHandlerData = Depends(BasePermission(responsibility=ResponsibilityType.VIEWER))
):
    document_repository: DocumentRepository = DocumentRepository(session)
    document = await document_repository.get_document_by_id(document_id)
    title, html = await get_html_content_from_blocks(document.id,
                                                     version_commit_id,
                                                     user,
                                                     session,
                                                     storage_client,
                                                     ya_disk)
    if export_type.DOCX:
        res = converters.docx.convert(html)
        headers = {"Content-Disposition": f'attachment; filename*=UTF-8\'\'"{title}"'}
        return Response(res, headers=headers, media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

    raise Exception


async def get_html_content_from_blocks(document_id: UUID,
                                       version_commit_id: Optional[str],
                                       user: WikiUserHandlerData,
                                       session: AsyncSession,
                                       storage_client: LakeFSClient,
                                       ya_disk: YaDisk) -> (str, str):
    document_repository: DocumentRepository = DocumentRepository(session)
    document = await document_repository.get_document_by_id(document_id, False)
    block_repository: BlockRepository = BlockRepository(session)
    # ! is wrong, the published version should be taken into account
    if user.wiki_api_client.responsibility == ResponsibilityType.ADMIN:
        list_blocks_document = await block_repository.get_all_block_by_document_id(document_id, version_commit_id)
    else:
        list_blocks_document = await block_repository.get_all_block_with_permissions_by_document_id(user.id,
                                                                                                    document_id,
                                                                                                    version_commit_id)
    content = []
    storage_service: VersioningWikiStorageService = VersioningWikiStorageService(storage_client)
    ya_storage = YaDiskAssetsStorage(ya_disk)
    asset_repository = AssetRepository(session)

    for block in list_blocks_document:
        if user.wiki_api_client.responsibility == ResponsibilityType.ADMIN or ObjectPermissionMode(block.permission_mode) >= ObjectPermissionMode.VIEW_AND_EXPORT:
            document_ids = await document_repository.get_list_ids_of_document_hierarchy(document)

            data = storage_service.get_content_document_block_in_workspace_storage(
                workspace_id=document.workspace_id,
                document_ids=document_ids,
                block_id=block.id,
                # ! is wrong, the published version should be taken into account
                version_commit_id=version_commit_id  # version_commit_id or document.current_published_version_commit_id
            )

            match TypeBlock(block.type_block):
                case TypeBlock.TEXT:
                    content.append(data)
                case TypeBlock.WIKI_LINK:
                    # rewrite the display
                    content.append(data)
                case TypeBlock.IMG:
                    link = ""
                    if data != "":
                        asset = await asset_repository.get_asset_by_id(UUID(data))
                        link = await ya_storage.download_asset(asset)
                    content.append(get_html_base_img_teg(link))
                case TypeBlock.FILE:
                    # rewrite the display
                    link = ""
                    if data != "":
                        asset = await asset_repository.get_asset_by_id(UUID(data))
                        link = await ya_storage.download_asset(asset)
                    content.append(get_html_base_file(link, f"file-{asset.id}"))
                case TypeBlock.VIDEO:
                    # rewrite the display
                    link = ""
                    if data != "":
                        asset = await asset_repository.get_asset_by_id(UUID(data))
                        link = await ya_storage.download_asset(asset)
                    content.append(get_html_base_file(link, f"video-{asset.id}"))

    title = f"document-{document.title}-{utcnow()}.pdf"
    return title, get_html_frame(content)


@document_export_router.post(
    "/export_doc",
    response_class=Response,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Export published version document",
    deprecated=True
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
