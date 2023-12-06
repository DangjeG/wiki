from datetime import datetime
from typing import Optional
from uuid import UUID

from wiki.models import WikiBase
from wiki.user.schemas import UserBaseInfoResponse
from wiki.wiki_workspace.schemas import ObjectPermissionInfoMixin


class CreateDocument(WikiBase):
    title: str
    workspace_id: UUID
    parent_document_id: Optional[UUID] = None


class DocumentInfoResponse(WikiBase, ObjectPermissionInfoMixin):
    id: UUID
    title: str
    workspace_id: UUID
    creator_user: UserBaseInfoResponse
    parent_document_id: Optional[UUID] = None
    created_at: datetime
    last_published_version_at: datetime


class DocumentNodeInfoResponse(WikiBase, ObjectPermissionInfoMixin):
    id: UUID
    title: str
    last_published_version_at: datetime
    children: Optional[list] = None
    is_have_children: bool = False
