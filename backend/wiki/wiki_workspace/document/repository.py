from uuid import UUID

from sqlalchemy import select

from wiki.database.repository import BaseRepository
from wiki.database.utils import menage_db_commit_method, CommitMode
from wiki.wiki_workspace.document.model import Document
from wiki.wiki_workspace.document.schemas import CreateDocument


class DocumentRepository(BaseRepository):

    @menage_db_commit_method(CommitMode.FLUSH)
    async def create_document(self, create_document: CreateDocument) -> Document:
        new_document = Document(
            title=create_document.title,
            workspace_id=create_document.workspace_id,
            creator_wiki_api_client=create_document.creator.id,
            parent_document_id=create_document.parent_document_id
        )

        self.session.add(new_document)

        return new_document

    async def get_all_document_by_workspace_id(self, workspace_id: UUID) -> list[Document]:
        document_query = await self.session.get(Document, workspace_id)
        result = document_query.scalars().all()
        return result

