from uuid import UUID

from pydantic import EmailStr

from wiki.models import WikiBase
from wiki.user.schemas import UserInfoResponse


class CreateWorkspace(WikiBase):
    title: str
    owner_user_email: EmailStr


class WorkspaceInfoResponse(WikiBase):
    id: UUID
    title: str
    owner_user: UserInfoResponse
