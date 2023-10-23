from sqlalchemy import select

from wiki.database.repository import BaseRepository
from wiki.database.utils import CommitMode, menage_db_commit_method
from wiki.wiki_workspace.model import Workspace
from wiki.wiki_workspace.schemas import CreateWorkspace


class WorkspaceRepository(BaseRepository):

    @menage_db_commit_method(CommitMode.FLUSH)
    async def create_workspace(self, create_workspace: CreateWorkspace) -> Workspace:

        new_workspace = Workspace(
            title=create_workspace.name,
            owner_wiki_api_client=create_workspace.owner.id
        )

        self.session.add(new_workspace)

        return new_workspace

    async def get_all_workspace(self) -> list[Workspace]:
        workspace_query = await self.session.execute(select(Workspace))
        result = workspace_query.scalars().all()
        return result
