from uuid import UUID

from fastapi import APIRouter, Depends
from lakefs_client.client import LakeFSClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from wiki.common.schemas import WikiUserHandlerData
from wiki.database.deps import get_db
from wiki.permissions.base import BasePermission
from wiki.user.utils import get_user_info
from wiki.wiki_api_client.enums import ResponsibilityType
from wiki.wiki_storage.deps import get_storage_client
from wiki.wiki_storage.services.versioning import VersioningWikiStorageService
from wiki.wiki_workspace.block.model import Block
from wiki.wiki_workspace.block.repository import BlockRepository
from wiki.wiki_workspace.document.model import Document
from wiki.wiki_workspace.document.repository import DocumentRepository
from wiki.wiki_workspace.repository import WorkspaceRepository
from wiki.wiki_workspace.versioning.model import VersionWorkspace
from wiki.wiki_workspace.versioning.repository import VersioningWorkspaceRepository
from wiki.wiki_workspace.versioning.schemas import (
    VersionWorkspaceInfoResponse,
    VersionWorkspaceInfoGraphResponse,
    VersionBlockInfo,
    VersionDocumentInfo
)
from wiki.wiki_workspace.versioning.utils import get_version_block_info_list, get_version_document_info_list

versioning_workspace_router = APIRouter()


@versioning_workspace_router.get(
    "/block/{block_id}/info",
    response_model=list[VersionBlockInfo],
    status_code=status.HTTP_200_OK,
    summary="Get info as a list of all versions block"
)
async def get_list_versions_document_block(
        block_id: UUID,
        session: AsyncSession = Depends(get_db),
        storage_client: LakeFSClient = Depends(get_storage_client),
        user: WikiUserHandlerData = Depends(BasePermission(responsibility=ResponsibilityType.VIEWER))
):
    block_repository: BlockRepository = BlockRepository(session)
    block: Block = await block_repository.get_block_by_id(block_id)
    document_repository: DocumentRepository = DocumentRepository(session)
    document: Document = await document_repository.get_document_by_id(block.document_id)
    document_ids = await document_repository.get_list_ids_of_document_hierarchy(document)

    storage_service: VersioningWikiStorageService = VersioningWikiStorageService(storage_client)
    resp = storage_service.get_version_document_block(document.workspace_id, document_ids, block_id)
    results: dict = resp["results"]
    return await get_version_block_info_list(results, block, session)


@versioning_workspace_router.get(
    "/document/{document_id}/info",
    response_model=list[VersionDocumentInfo],
    status_code=status.HTTP_200_OK,
    summary="Get info as a list of all versions document"
)
async def get_list_versions_document(
        document_id: UUID,
        session: AsyncSession = Depends(get_db),
        storage_client: LakeFSClient = Depends(get_storage_client),
        user: WikiUserHandlerData = Depends(BasePermission(responsibility=ResponsibilityType.VIEWER))
):
    document_repository: DocumentRepository = DocumentRepository(session)
    document: Document = await document_repository.get_document_by_id(document_id)
    document_ids = await document_repository.get_list_ids_of_document_hierarchy(document)

    storage_service: VersioningWikiStorageService = VersioningWikiStorageService(storage_client)
    resp = storage_service.get_versions_document(document.workspace_id, document_ids)
    results: dict = resp["results"]
    return await get_version_document_info_list(results, document, session)


@versioning_workspace_router.get(
    "/wp/{workspace_id}/info",
    response_model=list[VersionWorkspaceInfoResponse],
    status_code=status.HTTP_200_OK,
    summary="Get info as a list of all versions workspace",
    deprecated=True
)
async def get_list_info_versions_workspace(
        workspace_id: UUID,
        session: AsyncSession = Depends(get_db),
        user: WikiUserHandlerData = Depends(BasePermission(responsibility=ResponsibilityType.VIEWER))
):
    workspace_repository: WorkspaceRepository = WorkspaceRepository(session)
    workspace = await workspace_repository.get_workspace_by_id(workspace_id)
    version_repository: VersioningWorkspaceRepository = VersioningWorkspaceRepository(session)
    versions: list[VersionWorkspace] = await version_repository.get_all_versions_for_workspace(workspace)

    return [VersionWorkspaceInfoResponse(
        id=item.id,
        workspace_id=item.workspace_id,
        committer_user=await get_user_info(item.committer_user_id, session, is_full=False),
        branch=item.branch,
        created_at=item.created_at,
        parent_version_workspace_id=item.parent_version_id
    ) for item in versions]


@versioning_workspace_router.get(
    "/wp/{workspace_id}/info/graph",
    response_model=VersionWorkspaceInfoGraphResponse,
    status_code=status.HTTP_200_OK,
    summary="Get info as a list of all versions workspace",
    deprecated=True
)
async def get_graph_info_versions_workspace(
        workspace_id: UUID,
        session: AsyncSession = Depends(get_db),
        user: WikiUserHandlerData = Depends(BasePermission(responsibility=ResponsibilityType.VIEWER))
):
    workspace_repository: WorkspaceRepository = WorkspaceRepository(session)
    workspace = await workspace_repository.get_workspace_by_id(workspace_id)
    version_repository: VersioningWorkspaceRepository = VersioningWorkspaceRepository(session)
    versions: list[VersionWorkspace] = await version_repository.get_graph_all_versions_for_workspace(workspace)
    graph: VersionWorkspaceInfoGraphResponse = None
    for item in versions:
        graph = VersionWorkspaceInfoGraphResponse(
            id=item.id,
            workspace_id=item.workspace_id,
            committer_user=await get_user_info(item.committer_user_id, session, is_full=False),
            branch=item.branch,
            created_at=item.created_at,
            parent_version_workspace=graph
        )
    return graph
