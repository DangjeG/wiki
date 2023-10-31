from datetime import datetime
from typing import Optional
from uuid import UUID

from wiki.models import WikiBase
from wiki.user.schemas import UserFullInfoResponse, UserBaseInfoResponse


class CreateDocument(WikiBase):
    title: str
    workspace_id: UUID
    parent_document_id: Optional[UUID] = None


class DocumentInfoResponse(WikiBase):
    id: UUID
    title: str
    workspace_id: UUID
    creator_user: UserBaseInfoResponse
    parent_document_id: Optional[UUID] = None
    created_at: datetime


class DocumentNodeInfoResponse(WikiBase):
    id: UUID
    title: str
    children: Optional[list] = None
