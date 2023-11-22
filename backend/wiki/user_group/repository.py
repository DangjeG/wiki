from typing import Optional
from uuid import UUID

from sqlalchemy import select, and_
from starlette import status

from wiki.common.exceptions import WikiException, WikiErrorCode
from wiki.database.repository import BaseRepository
from wiki.database.utils import (
    CommitMode,
    menage_db_commit_method,
    NotFoundResultMode,
    menage_db_not_found_result_method
)
from wiki.user.models import User
from wiki.user_group.models import Group, UserGroup
from wiki.user_group.schemas import GroupOptionalInfo, CreateGroup
from wiki.user_group.utils import get_group_filters


class GroupRepository(BaseRepository):
    _group_not_found_exception = WikiException(
        message="Group not found.",
        error_code=WikiErrorCode.USER_GROUP_NOT_FOUND,
        http_status_code=status.HTTP_404_NOT_FOUND
    )
    _user_already_member_group_exception = WikiException(
        message="User already member group.",
        error_code=WikiErrorCode.USER_ALREADY_MEMBER_GROUP,
        http_status_code=status.HTTP_409_CONFLICT
    )
    _user_not_member_group = WikiException(
        message="User not member group.",
        error_code=WikiErrorCode.USER_NOT_MEMBER_GROUP,
        http_status_code=status.HTTP_409_CONFLICT
    )

    @menage_db_not_found_result_method(NotFoundResultMode.EXCEPTION, ex=_group_not_found_exception)
    async def get_group_by_id(self, group_id: UUID, is_only_existing: bool = True) -> Group:
        whereclause = [Group.id == group_id]
        if is_only_existing:
            whereclause.append(Group.is_deleted == False)
        st = select(Group).where(and_(*whereclause))
        result = (await self.session.execute(st)).scalar()

        return result

    async def get_all_groups_filter(self, filter_group: GroupOptionalInfo, is_only_existing: bool = True) -> list[Group]:
        filters = get_group_filters(filter_group)
        if is_only_existing:
            filters.append(Group.is_deleted == False)

        st = select(Group).where(and_(*filters))
        result = await self.session.execute(st)

        return result.scalars().all()

    async def get_members_users_group(self, group: Group, is_members_only_existing: bool = True) -> list[User]:
        filters = [UserGroup.group_id == group.id]
        if is_members_only_existing:
            filters.append(UserGroup.is_deleted == False)
        st = select(User).join(UserGroup).filter(and_(*filters))
        result = (await self.session.execute(st)).scalars().all()

        return result

    async def get_groups_for_user(self,
                                  user: User,
                                  filter_group: GroupOptionalInfo,
                                  is_only_existing: bool = True) -> list[Group]:
        filters = get_group_filters(filter_group)
        filters.append(UserGroup.user_id == user.id)
        if is_only_existing:
            filters.append(Group.is_deleted == False)
        st = select(Group).join(UserGroup).filter(and_(*filters))
        result = (await self.session.execute(st)).scalars().all()

        return result

    @menage_db_not_found_result_method(NotFoundResultMode.NONE)
    async def get_user_group(self, group: Group, user: User, is_only_existing: bool = True) -> Optional[UserGroup]:
        whereclause = [UserGroup.group_id == group.id, UserGroup.user_id == user.id]
        if is_only_existing:
            whereclause.append(UserGroup.is_deleted == False)
        st = select(UserGroup).where(and_(*whereclause))
        result = (await self.session.execute(st)).scalar()

        return result

    @menage_db_commit_method(CommitMode.FLUSH)
    async def add_user_in_group(self, group_id: UUID, user: User):
        group = await self.get_group_by_id(group_id)
        user_group = await self.get_user_group(group, user)
        if user_group is not None:
            raise self._user_already_member_group_exception
        new_user_group = UserGroup(
            group_id=group.id,
            user_id=user.id
        )
        self.session.add(new_user_group)

    @menage_db_commit_method(CommitMode.FLUSH)
    async def remove_user_from_group(self, group_id: UUID, user: User):
        group = await self.get_group_by_id(group_id)
        user_group: UserGroup = await self.get_user_group(group, user)
        if user_group is None:
            raise self._user_not_member_group
        user_group.is_deleted = True
        self.session.add(user_group)

    @menage_db_commit_method(CommitMode.FLUSH)
    async def create_group(self, create_group: CreateGroup) -> Group:
        new_group = Group(
            name=create_group.name,
            description=create_group.description,
            is_members_can_add_to_group=create_group.is_members_can_add_to_group
        )
        self.session.add(new_group)

        return new_group

    @menage_db_commit_method(CommitMode.FLUSH)
    async def update_group(self,
                           group_id: UUID,
                           update_group: GroupOptionalInfo) -> Group:
        group = await self.get_group_by_id(group_id)

        if update_group.name is not None:
            group.name = update_group.name
        if update_group.description is not None:
            group.description = update_group.description
        if update_group.is_members_can_add_to_group is not None:
            group.is_members_can_add_to_group = update_group.is_members_can_add_to_group
        self.session.add(group)

        return group

    @menage_db_commit_method(CommitMode.FLUSH)
    async def delete_group(self,
                           group_id: UUID):
        group = await self.get_group_by_id(group_id)
        group.is_deleted = True
        self.session.add(group)
