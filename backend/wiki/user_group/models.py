from sqlalchemy import Column, Uuid, String, ForeignKey, Boolean
from uuid_extensions import uuid7

from wiki.common.models import DeletedMixin
from wiki.database.core import Base
from wiki.user.schemas import UserBaseInfoResponse
from wiki.user_group.schemas import GroupInfo, GroupInfoWithUsers


class Group(Base, DeletedMixin):
    id = Column(Uuid, default=uuid7, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String(256), nullable=True)
    is_members_can_add_to_group = Column(Boolean, nullable=False, default=False)

    def get_group_info(self) -> GroupInfo:
        return GroupInfo(
            id=self.id,
            name=self.name,
            description=self.description,
            is_members_can_add_to_group=self.is_members_can_add_to_group,
            created_at=self.created_at,
            updated_at=self.updated_at
        )

    def get_group_info_with_members(self, members: list[UserBaseInfoResponse]):
        return GroupInfoWithUsers(
            id=self.id,
            name=self.name,
            description=self.description,
            is_members_can_add_to_group=self.is_members_can_add_to_group,
            created_at=self.created_at,
            updated_at=self.updated_at,
            members=members
        )


class UserGroup(Base, DeletedMixin):
    id = Column(Uuid, default=uuid7, primary_key=True, nullable=False)
    group_id = Column(ForeignKey("group.id"), nullable=False)
    user_id = Column(ForeignKey("user.id"), nullable=False)
