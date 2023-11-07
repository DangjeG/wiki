from typing import Optional
from uuid import UUID

from wiki.models import WikiBase
from wiki.wiki_workspace.document_template.emums import DocumentTemplateType


class CreateDocumentTemplate(WikiBase):
    title: str
    description: str
    document_id: UUID
    orig_commit_id: UUID
    document_template_type: DocumentTemplateType
    creator_user_id: Optional[UUID] = None

class DocumentTemplateInfoResponse(WikiBase):
    id: UUID
    title: str
    description: str
    document_id: UUID
    document_template_type: DocumentTemplateType
    creator_user_id: Optional[UUID] = None

class DocumentTemplateFilter(WikiBase):
    title: Optional[str] = None
    description: Optional[str] = None
    document_template_type: Optional[DocumentTemplateType] = None
    creator_user_id: Optional[UUID] = None
