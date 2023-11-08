from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from wiki.user.utils import get_user_info
from wiki.wiki_workspace.model import Workspace
from wiki.wiki_workspace.repository import WorkspaceRepository
from wiki.wiki_workspace.schemas import WorkspaceInfoResponse


async def get_workspace_info(workspace: UUID, session: AsyncSession):
    workspace_repository = WorkspaceRepository(session)
    workspace_db: Workspace = await workspace_repository.get_workspace_by_id(workspace)

    return WorkspaceInfoResponse(
        id=workspace_db.id,
        title=workspace_db.title,
        owner_user=await get_user_info(workspace_db.owner_user_id, session, is_full=False)
    )
