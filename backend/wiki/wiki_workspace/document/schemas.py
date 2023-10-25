from typing import Optional
from uuid import UUID

from wiki.models import WikiBase
from wiki.user.schemas import UserInfoResponse


class CreateDocument(WikiBase):
    title: str
    workspace_id: UUID
    parent_document_id: Optional[UUID] = None


class DocumentInfoResponse(WikiBase):
    id: UUID
    title: str
    workspace_id: UUID
    creator_user: UserInfoResponse
    parent_document_id: Optional[UUID] = None


class DocumentNodeInfoResponse(WikiBase):
    id: UUID
    title: str
    children: Optional[list] = None
