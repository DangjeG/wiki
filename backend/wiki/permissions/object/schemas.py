from datetime import datetime
from typing import Optional
from uuid import UUID

from wiki.models import WikiBase
from wiki.permissions.object.enums import ObjectPermissionMode
from wiki.user.schemas import UserBaseInfoResponse
from wiki.user_group.schemas import GroupInfo
from wiki.wiki_api_client.enums import ResponsibilityType


class BaseCreateObjectPermission(WikiBase):
    mode: ObjectPermissionMode = ObjectPermissionMode.HIDDEN_INACCESSIBLE


class CreateGeneralObjectPermission(BaseCreateObjectPermission):
    required_responsibility: ResponsibilityType


class CreateGroupObjectPermission(BaseCreateObjectPermission):
    group_id: UUID


class CreateIndividualObjectPermission(BaseCreateObjectPermission):
    user_id: UUID


class UpdateBaseObjectPermission(WikiBase):
    mode: Optional[ObjectPermissionMode] = None


class UpdateGeneralObjectPermission(UpdateBaseObjectPermission):
    required_responsibility: Optional[ResponsibilityType] = None


class BaseObjectPermissionInfo(WikiBase):
    id: UUID
    mode: ObjectPermissionMode
    object_id: UUID
    created_at: datetime
    updated_at: datetime


class GeneralObjectPermissionInfo(BaseObjectPermissionInfo):
    required_responsibility: ResponsibilityType


class GroupObjectPermissionInfo(BaseObjectPermissionInfo):
    # members can add users to the group, giving them the same permissions
    group: GroupInfo


class IndividualObjectPermissionInfo(BaseObjectPermissionInfo):
    user: UserBaseInfoResponse
