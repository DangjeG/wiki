from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from wiki.database.deps import get_db
from wiki.wiki_api_client.models import WikiApiClient
from wiki.wiki_api_client.repository import WikiApiClientRepository
from wiki.wiki_workspace.repository import WorkspaceRepository
from wiki.wiki_workspace.schemas import WorkspaceResponse, CreateWorkspace, WorkspaceInfo

workspace_router = APIRouter()

@workspace_router.post(
    "/workspace",
    response_model=WorkspaceResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Create workspace"
)
async def create_workspace(
        workspace: CreateWorkspace,
        wiki_api_client: WikiApiClient,
        session: AsyncSession = Depends(get_db)
):
    workspace_repository: WorkspaceRepository = WorkspaceRepository(session)
    workspace.owner = wiki_api_client
    await workspace_repository.create_workspace(workspace)

    return WorkspaceResponse(
        title=workspace.title
    )

@workspace_router.get(
    "/workspace",
    response_model=list[WorkspaceInfo],
    status_code=status.HTTP_202_ACCEPTED,
    summary="Get all workspace"
)
async def get_workspaces(
        session: AsyncSession = Depends(get_db)
):
    workspace_repository: WorkspaceRepository = WorkspaceRepository(session)
    wiki_api_client_repository: WikiApiClientRepository = WikiApiClientRepository(session)

    workspaces = await workspace_repository.get_all_workspace()

    result_workspace: list[WorkspaceInfo] = []
    for ws in workspaces:
        append_workspace = WorkspaceInfo(
            id=ws.id,
            title=ws.title,
            owner=await wiki_api_client_repository.get_wiki_api_client_by_id(ws.id)
        )
        result_workspace.append(append_workspace)

    return result_workspace
