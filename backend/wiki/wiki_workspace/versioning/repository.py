from typing import Optional
from uuid import UUID

from sqlalchemy import select, and_, label
from starlette import status

from wiki.common.exceptions import WikiException, WikiErrorCode
from wiki.database.repository import BaseRepository
from wiki.database.utils import (
    menage_db_commit_method,
    CommitMode,
    menage_db_not_found_result_method,
    NotFoundResultMode
)
from wiki.user.models import User
from wiki.wiki_workspace.model import Workspace
from wiki.wiki_workspace.versioning.model import VersionWorkspace


class VersioningWorkspaceRepository(BaseRepository):
    _version_workspace_not_found_exception = WikiException(
        message="Version workspace not found.",
        error_code=WikiErrorCode.VERSION_WORKSPACE_NOT_FOUND,
        http_status_code=status.HTTP_404_NOT_FOUND
    )
    _root_version_workspace_not_found_exception = WikiException(
        message="Root version workspace not found.",
        error_code=WikiErrorCode.ROOT_VERSION_WORKSPACE_NOT_FOUND,
        http_status_code=status.HTTP_404_NOT_FOUND
    )

    @menage_db_commit_method(CommitMode.FLUSH)
    async def create_version(self,
                             commit_id: str,
                             workspace: Workspace,
                             committer_user: User,
                             branch: str,
                             parent_version: Optional[VersionWorkspace] = None) -> VersionWorkspace:
        new_version = VersionWorkspace(
            commit_id=commit_id,
            workspace_id=workspace.id,
            committer_user_id=committer_user.id,
            branch=branch,
            parent_version=parent_version.id if parent_version is not None else None
        )
        self.session.add(new_version)

        return new_version

    @menage_db_not_found_result_method(NotFoundResultMode.EXCEPTION, ex=_version_workspace_not_found_exception)
    async def get_version_by_commit_id(self, commit_id: str) -> VersionWorkspace:
        return (await self.session.execute(
            select(VersionWorkspace)
            .where(VersionWorkspace.commit_id == commit_id)
        )).scalar()

    @menage_db_not_found_result_method(NotFoundResultMode.EXCEPTION, ex=_version_workspace_not_found_exception)
    async def get_version_by_id(self, version_id: UUID) -> VersionWorkspace:
        return await self.session.get(VersionWorkspace, version_id)

    async def get_all_versions_for_workspace(self, workspace: Workspace) -> list[VersionWorkspace]:
        return (await self.session.execute(
            select(VersionWorkspace)
            .where(VersionWorkspace.workspace_id == workspace.id)
        )).scalars().all()

    @menage_db_not_found_result_method(NotFoundResultMode.EXCEPTION, ex=_root_version_workspace_not_found_exception)
    async def get_root_version_for_workspace(self, workspace: Workspace) -> VersionWorkspace:
        return (await self.session.execute(
            select(VersionWorkspace)
            .where(and_(VersionWorkspace.workspace_id == workspace.id,
                        VersionWorkspace.parent_version_id == None))
        )).scalar()

    async def get_graph_all_versions_for_workspace(self, workspace: Workspace) -> list[VersionWorkspace]:
        """
        WITH RECURSIVE version_workspace_hierarchy AS
        (SELECT id, commit_id, workspace_id,
                committer_user_id, branch, created_at,
                updated_at, parent_version_id, 0 AS level
         FROM version_workspace where parent_version_id IS NULL
         UNION ALL
         SELECT vw.id, vw.commit_id, vw.workspace_id,
                vw.committer_user_id, vw.branch, vw.created_at,
                vw.updated_at, vw.parent_version_id, vwh.level + 1
                FROM version_workspace vw
                INNER JOIN version_workspace_hierarchy vwh ON vw.parent_version_id = vwh.id)
        SELECT id, commit_id, workspace_id,
               committer_user_id, branch, created_at,
               updated_at, parent_version_id
        FROM version_workspace_hierarchy ORDER BY level;
        """
        version_workspace_hierarchy = (
            select(
                VersionWorkspace.id,
                VersionWorkspace.commit_id,
                VersionWorkspace.workspace_id,
                VersionWorkspace.committer_user_id,
                VersionWorkspace.branch,
                VersionWorkspace.created_at,
                VersionWorkspace.updated_at,
                VersionWorkspace.parent_version_id,
                label('level', 0)
            ).filter(VersionWorkspace.parent_version_id.is_(None)).cte(recursive=True))

        version_workspace_hierarchy_alias = version_workspace_hierarchy.alias()

        version_workspace_hierarchy = version_workspace_hierarchy.union_all(
            select(
                VersionWorkspace.id,
                VersionWorkspace.commit_id,
                VersionWorkspace.workspace_id,
                VersionWorkspace.committer_user_id,
                VersionWorkspace.branch,
                VersionWorkspace.created_at,
                VersionWorkspace.updated_at,
                VersionWorkspace.parent_version_id,
                (version_workspace_hierarchy_alias.c.level + 1).label('level')
            ).join(
                version_workspace_hierarchy_alias,
                VersionWorkspace.parent_version_id == version_workspace_hierarchy_alias.c.id
            )
        )

        query = select(
            version_workspace_hierarchy.c.id,
            version_workspace_hierarchy.c.commit_id,
            version_workspace_hierarchy.c.workspace_id,
            version_workspace_hierarchy.c.committer_user_id,
            version_workspace_hierarchy.c.branch,
            version_workspace_hierarchy.c.created_at,
            version_workspace_hierarchy.c.updated_at,
            version_workspace_hierarchy.c.parent_version_id
        ).order_by(version_workspace_hierarchy.c.level)

        results = (await self.session.execute(query)).all()
        return results
