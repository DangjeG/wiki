from uuid import UUID

from fastapi import APIRouter, Depends
from lakefs_client.client import LakeFSClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from wiki.common.schemas import WikiUserHandlerData
from wiki.database.deps import get_db
from wiki.permissions.base import BasePermission
from wiki.user.models import User
from wiki.user.repository import UserRepository
from wiki.user.utils import get_user_info
from wiki.wiki_api_client.enums import ResponsibilityType
from wiki.wiki_storage.deps import get_storage_client
from wiki.wiki_storage.services.base import BaseWikiStorageService
from wiki.wiki_workspace.model import Workspace
from wiki.wiki_workspace.repository import WorkspaceRepository
from wiki.wiki_workspace.schemas import CreateWorkspace, WorkspaceInfoResponse

workspace_router = APIRouter()


@workspace_router.post(
    "/",
    response_model=WorkspaceInfoResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Create workspace"
)
async def create_workspace(
        workspace_create: CreateWorkspace,
        session: AsyncSession = Depends(get_db),
        storage_client: LakeFSClient = Depends(get_storage_client),
        user: WikiUserHandlerData = Depends(BasePermission(responsibility=ResponsibilityType.VIEWER))
):
    workspace_repository: WorkspaceRepository = WorkspaceRepository(session)

    user_repository: UserRepository = UserRepository(session)
    user_db: User = await user_repository.get_user_by_id(user.id)
    workspace: Workspace = await workspace_repository.create_workspace(workspace_create.title, user_db.id)

    storage_service: BaseWikiStorageService = BaseWikiStorageService(storage_client)
    storage_service.create_workspace_storage(workspace.id)

    return WorkspaceInfoResponse(
        id=workspace.id,
        title=workspace.title,
        owner_user=await get_user_info(user_db.id, session, is_full=False)
    )


@workspace_router.get(
    "/all",
    response_model=list[WorkspaceInfoResponse],
    status_code=status.HTTP_200_OK,
    summary="Get all workspace"
)
async def get_workspaces(
        session: AsyncSession = Depends(get_db),
        user: WikiUserHandlerData = Depends(BasePermission(responsibility=ResponsibilityType.VIEWER))
):
    workspace_repository: WorkspaceRepository = WorkspaceRepository(session)
    workspaces = await workspace_repository.get_all_workspace()

    result_workspace: list[WorkspaceInfoResponse] = []
    for ws in workspaces:
        append_workspace = WorkspaceInfoResponse(
            id=ws.id,
            title=ws.title,
            owner_user=await get_user_info(ws.owner_user_id, session, is_full=False)
        )
        result_workspace.append(append_workspace)

    return result_workspace


@workspace_router.get(
    "/info",
    response_model=WorkspaceInfoResponse,
    status_code=status.HTTP_200_OK,
    summary="Get workspace info"
)
async def get_workspace_info(
        workspace_id: UUID,
        session: AsyncSession = Depends(get_db),
        user: WikiUserHandlerData = Depends(BasePermission(responsibility=ResponsibilityType.VIEWER))
):
    workspace_repository: WorkspaceRepository = WorkspaceRepository(session)
    workspace = await workspace_repository.get_workspace_by_id(workspace_id)

    return WorkspaceInfoResponse(
        id=workspace.id,
        title=workspace.title,
        owner_user=await get_user_info(workspace.owner_user_id, session, is_full=False)
    )
