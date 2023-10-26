from uuid import UUID

from pydantic import EmailStr

from wiki.models import WikiBase
from wiki.user.schemas import UserBaseInfoResponse


class CreateWorkspace(WikiBase):
    title: str


class WorkspaceInfoResponse(WikiBase):
    id: UUID
    title: str
    owner_user: UserBaseInfoResponse
