from typing import Optional
from uuid import UUID

from sqlalchemy import Column, Uuid, ForeignKey, Boolean, String
from uuid_extensions import uuid7

from wiki.common.models import EnabledDeletedMixin
from wiki.database.core import Base
from wiki.wiki_workspace.document_template.emums import DocumentTemplateType


class DocumentTemplate(Base, EnabledDeletedMixin):
    id = Column(Uuid, default=uuid7, primary_key=True, nullable=False)

    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    is_default_template = Column(Boolean, nullable=False, default=False)
    document_template_type = Column(String, nullable=False, default=str(DocumentTemplateType.START))

    document_id = Column(ForeignKey("document.id"), nullable=False)
    creator_user_id = Column(ForeignKey("user.id"), nullable=True)
    orig_commit_id = Column(String(64), nullable=False)

    def __init__(self,
                 document_id: UUID,
                 title: str,
                 description: str,
                 orig_commit_id: UUID,
                 document_template_type: DocumentTemplateType,
                 creator_user_id: Optional[UUID] = None):
        self.document_id = document_id
        self.title = title
        self.description = description
        self.orig_commit_id = orig_commit_id
        self.document_template_type = str(document_template_type)
        if creator_user_id is None:
            self.is_default_template = True
        else:
            self.creator_user_id = creator_user_id
