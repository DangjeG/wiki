from datetime import datetime
from typing import Optional
from uuid import UUID

from wiki.models import WikiBase
from wiki.user.schemas import UserBaseInfoResponse


class GroupOptionalInfo(WikiBase):
    name: Optional[str] = None
    description: Optional[str] = None
    is_members_can_add_to_group: Optional[bool] = None


class CreateGroup(WikiBase):
    name: str
    description: Optional[str] = None
    is_members_can_add_to_group: bool = False


class GroupInfo(WikiBase):
    id: UUID
    name: str
    description: Optional[str] = None
    is_members_can_add_to_group: bool
    created_at: datetime
    updated_at: datetime


class GroupInfoWithUsers(GroupInfo):
    members: list[UserBaseInfoResponse]
