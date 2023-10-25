from typing import Optional
from uuid import UUID

from sqlalchemy import select
from starlette import status

from wiki.common.exceptions import WikiException, WikiErrorCode
from wiki.database.repository import BaseRepository
from wiki.database.utils import (
    menage_db_commit_method,
    CommitMode,
    menage_db_not_found_result_method,
    NotFoundResultMode
)
from wiki.wiki_workspace.document.model import Document


class DocumentRepository(BaseRepository):
    _document_not_found_exception = WikiException(
        message="Document not found.",
        error_code=WikiErrorCode.DOCUMENT_NOT_FOUND,
        http_status_code=status.HTTP_404_NOT_FOUND
    )

    @menage_db_not_found_result_method(NotFoundResultMode.EXCEPTION, ex=_document_not_found_exception)
    async def get_document_by_id(self, document_id: UUID) -> Document:
        return await self.session.get(Document, document_id)

    @menage_db_commit_method(CommitMode.FLUSH)
    async def create_document(self,
                              title: str,
                              workspace_id: UUID,
                              creator_user_id: UUID,
                              parent_document_id: Optional[UUID] = None) -> Document:
        new_document = Document(
            title=title,
            workspace_id=workspace_id,
            creator_user_id=creator_user_id,
            parent_document_id=parent_document_id
        )

        self.session.add(new_document)

        return new_document

    async def get_all_document_by_workspace_id(self, workspace_id: UUID) -> list[Document]:
        document_query = await self.session.execute(select(Document).where(Document.workspace_id == workspace_id))
        result = document_query.scalars().all()
        return result
