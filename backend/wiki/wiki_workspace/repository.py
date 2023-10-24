from uuid import UUID

from sqlalchemy import select
from starlette import status

from wiki.common.exceptions import WikiException, WikiErrorCode
from wiki.database.repository import BaseRepository
from wiki.database.utils import CommitMode, menage_db_commit_method, NotFoundResultMode, \
    menage_db_not_found_result_method
from wiki.wiki_workspace.model import Workspace


class WorkspaceRepository(BaseRepository):
    _workspace_not_found_exception = WikiException(
        message="Document not found.",
        error_code=WikiErrorCode.WORKSPACE_NOT_FOUND,
        http_status_code=status.HTTP_404_NOT_FOUND
    )

    @menage_db_not_found_result_method(NotFoundResultMode.EXCEPTION, ex=_workspace_not_found_exception)
    async def get_workspace_by_id(self, workspace_id: UUID) -> Workspace:
        return await self.session.get(Workspace, workspace_id)

    @menage_db_commit_method(CommitMode.FLUSH)
    async def create_workspace(self, title: str, owner_user_id: UUID) -> Workspace:

        new_workspace = Workspace(
            title=title,
            owner_user_id=owner_user_id
        )

        self.session.add(new_workspace)

        return new_workspace

    async def get_all_workspace(self) -> list[Workspace]:
        workspace_query = await self.session.execute(select(Workspace))
        result = workspace_query.scalars().all()
        return result
