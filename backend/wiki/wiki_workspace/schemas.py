from uuid import UUID

from wiki.models import WikiBase
from wiki.permissions.object.enums import ObjectPermissionMode
from wiki.user.schemas import UserBaseInfoResponse


class CreateWorkspace(WikiBase):
    title: str


class ObjectPermissionInfoMixin:
    permission_mode: ObjectPermissionMode


class WorkspaceInfoResponse(WikiBase, ObjectPermissionInfoMixin):
    id: UUID
    title: str
    owner_user: UserBaseInfoResponse
