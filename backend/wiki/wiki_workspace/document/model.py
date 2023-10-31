from typing import Optional
from uuid import UUID

from sqlalchemy import Column, Uuid, ForeignKey, String
from uuid_extensions import uuid7

from wiki.common.models import EnabledDeletedMixin
from wiki.database.core import Base


class Document(Base, EnabledDeletedMixin):
    id = Column(Uuid, default=uuid7, primary_key=True, nullable=False)

    title = Column(String, nullable=False)

    creator_user_id = Column(ForeignKey("user.id"), nullable=False)
    workspace_id = Column(ForeignKey("workspace.id"), nullable=False)
    parent_document_id = Column(ForeignKey("document.id"), nullable=True)

    current_published_version_commit_id = Column(String(64), nullable=True)

    def __init__(self,
                 title: str,
                 workspace_id: UUID,
                 creator_user_id: UUID,
                 parent_document_id: Optional[UUID] = None,
                 current_published_version_commit_id: Optional[str] = None):
        self.title = title
        self.workspace_id = workspace_id
        self.creator_user_id = creator_user_id
        self.parent_document_id = parent_document_id
        self.current_published_version_commit_id = current_published_version_commit_id
