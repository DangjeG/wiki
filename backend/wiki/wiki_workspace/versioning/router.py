from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from wiki.common.schemas import WikiUserHandlerData
from wiki.database.deps import get_db
from wiki.permissions.base import BasePermission
from wiki.user.utils import get_user_info
from wiki.wiki_api_client.enums import ResponsibilityType
from wiki.wiki_workspace.repository import WorkspaceRepository
from wiki.wiki_workspace.versioning.model import VersionWorkspace
from wiki.wiki_workspace.versioning.repository import VersioningWorkspaceRepository
from wiki.wiki_workspace.versioning.schemas import (
    VersionWorkspaceInfoResponse,
    VersionWorkspaceInfoGraphResponse
)

versioning_workspace_router = APIRouter()


@versioning_workspace_router.get(
    "/wp/{workspace_id}/info",
    response_model=list[VersionWorkspaceInfoResponse],
    status_code=status.HTTP_200_OK,
    summary="Get info as a list of all versions workspace"
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
    summary="Get info as a list of all versions workspace"
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
