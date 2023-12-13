from typing import Optional
from uuid import UUID

from sqlalchemy import select, Result, and_, Row
from sqlalchemy.orm import join
from sqlalchemy.sql.functions import coalesce
from starlette import status

from wiki.common.exceptions import WikiException, WikiErrorCode
from wiki.database.repository import BaseRepository
from wiki.database.utils import CommitMode, menage_db_commit_method, NotFoundResultMode, \
    menage_db_not_found_result_method
from wiki.permissions.object.enums import ObjectPermissionMode
from wiki.permissions.object.general.models import GeneralWorkspacePermission
from wiki.permissions.object.group.models import GroupWorkspacePermission
from wiki.permissions.object.individual.models import IndividualWorkspacePermission
from wiki.user.models import User
from wiki.user_group.models import Group, UserGroup
from wiki.wiki_api_client.models import WikiApiClient
from wiki.wiki_workspace.block.model import Block, VersionBlock
from wiki.wiki_workspace.model import Workspace


class ObjectRepository(BaseRepository):
    async def _get_result_object_with_permission(self,
                                                 object_class,
                                                 individual_permission_class,
                                                 group_permission_class,
                                                 general_permission_class,
                                                 user_id: UUID,
                                                 version_commit_id: Optional[str] = None,
                                                 *whereclause) -> Result:
        """
        SELECT wp.id,
               wp.title,
               wp.owner_user_id,
               wp.is_enabled,
               wp.is_deleted,
               wp.created_at,
               wp.updated_at,
               COALESCE(iwp.mode, grwp.mode, gwp.mode, 'HIDDEN_INACCESSIBLE') AS mode
        FROM workspace wp
        LEFT JOIN individual_workspace_permission iwp
            ON wp.id = iwp.object_id AND
            iwp.user_id = '<user_id>'
        LEFT JOIN group_workspace_permission grwp
            ON wp.id = grwp.object_id AND
            grwp.group_id IN (
                select g.id from "group" g
                    join user_group usg on g.id = usg.group_id
                where usg.user_id = 'user_id')
        LEFT JOIN general_workspace_permission gwp
            ON wp.id = gwp.object_id AND
            gwp.mode IN (
                select wac.responsibility from "user" u
                    join wiki_api_client wac on wac.id = u.wiki_api_client_id
                where u.id = '065384c5-f93a-7239-8000-fa00622cb6bc');
        """
        subquery_1 = select(Group.id).select_from(
            join(Group, UserGroup, Group.id == UserGroup.group_id)).where(
            UserGroup.user_id == user_id)
        subquery_2 = select(WikiApiClient.responsibility).select_from(
            join(User, WikiApiClient, WikiApiClient.id == User.wiki_api_client_id)).where(
            User.id == user_id)

        query = (select(
            object_class.__table__.columns,
            coalesce(individual_permission_class.mode,
                     group_permission_class.mode,
                     general_permission_class.mode,
                     str(ObjectPermissionMode.HIDDEN_INACCESSIBLE)).label("permission_mode")
        ).join(
            individual_permission_class,
            and_(
                object_class.id == individual_permission_class.object_id,
                individual_permission_class.user_id == user_id
            ),
            isouter=True
        ).join(
            group_permission_class,
            and_(
                object_class.id == group_permission_class.object_id,
                group_permission_class.group_id.in_(subquery_1)
            ),
            isouter=True
        ).join(
            general_permission_class,
            and_(
                object_class.id == general_permission_class.object_id,
                general_permission_class.required_responsibility.in_(subquery_2)
            ),
            isouter=True
        ))
        if version_commit_id is not None and object_class == Block:
            query = (query.join(VersionBlock, Block.id == VersionBlock.block_id)
                     .where(and_(VersionBlock.version_commit_id == version_commit_id,
                                 *whereclause)))
        else:
            query = query.where(and_(*whereclause))

        return await self.session.execute(query)


class WorkspaceRepository(ObjectRepository):
    workspace_not_found_exception = WikiException(
        message="Workspace not found.",
        error_code=WikiErrorCode.WORKSPACE_NOT_FOUND,
        http_status_code=status.HTTP_404_NOT_FOUND
    )

    async def _get_result_workspaces_with_permission(self, user_id: UUID, *whereclause):
        return await self._get_result_object_with_permission(
            Workspace,
            IndividualWorkspacePermission,
            GroupWorkspacePermission,
            GeneralWorkspacePermission,
            user_id,
            None,
            *whereclause
        )

    async def get_workspaces_with_permission(self, user_id: UUID) -> list[Row]:
        res = await self._get_result_workspaces_with_permission(user_id)
        return res.all()

    @menage_db_not_found_result_method(NotFoundResultMode.EXCEPTION, ex=workspace_not_found_exception)
    async def get_workspace_with_permission_by_id(self, user_id: UUID, workspace_id: UUID) -> Row:
        res = await self._get_result_workspaces_with_permission(user_id, Workspace.id == workspace_id)
        arr = res.all()
        return arr[0] if len(arr) > 0 else None

    @menage_db_not_found_result_method(NotFoundResultMode.EXCEPTION, ex=workspace_not_found_exception)
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
