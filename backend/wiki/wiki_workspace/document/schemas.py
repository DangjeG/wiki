from typing import Optional
from uuid import UUID

from wiki.models import WikiBase
from wiki.wiki_api_client.models import WikiApiClient


class CreateDocument(WikiBase):
    title: str
    workspace_id: UUID
    creator: WikiApiClient
    parent_document_id: Optional[UUID] = None

class DocumentResponse(WikiBase):
    title: str

class DocumentInfo(WikiBase):
    title: str
    workspace_id: UUID
    creator: WikiApiClient
    parent_document_id: Optional[UUID] = None
