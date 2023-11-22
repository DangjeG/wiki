from typing import Optional
from uuid import UUID

from sqlalchemy import select, and_
from starlette import status

from wiki.common.exceptions import WikiException, WikiErrorCode
from wiki.database.repository import BaseRepository
from wiki.database.utils import CommitMode, menage_db_commit_method, NotFoundResultMode, \
    menage_db_not_found_result_method
from wiki.user_group.models import Group
from wiki.user_group.schemas import GroupFilter


class GroupRepository(BaseRepository):
    _group_not_found_exception = WikiException(
        message="Group not found.",
        error_code=WikiErrorCode.USER_GROUP_NOT_FOUND,
        http_status_code=status.HTTP_404_NOT_FOUND
    )

    @menage_db_not_found_result_method(NotFoundResultMode.EXCEPTION, ex=_group_not_found_exception)
    async def get_group_by_id(self, group_id: UUID) -> Group:
        group_query = await self.session.get(Group, group_id)
        return group_query

    async def get_all_groups_filter(self, filter_group: GroupFilter) -> list[Group]:
        filters = []
        if filter_group.name is not None:
            filters.append(select(Group.name.ilike(f"%{filter_group.name}%")))
        if filter_group.description is not None:
            filters.append(select(Group.description.ilike(f"%{filter_group.description}%")))

        result = await self.session.execute(select(Group).where(and_(*filters)))

        return result.scalars().all()

    @menage_db_commit_method(CommitMode.FLUSH)
    async def create_group(self,
                           name: str,
                           description: Optional[str] = None,
                           is_members_can_add_to_group: bool = False) -> Group:
        new_group = Group(
            name=name,
            description=description,
            is_members_can_add_to_group=is_members_can_add_to_group
        )
        self.session.add(new_group)

        return new_group
