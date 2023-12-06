from typing import Optional
from uuid import UUID

from sqlalchemy import select, and_
from starlette import status

from wiki.common.exceptions import WikiException, WikiErrorCode
from wiki.database.utils import (
    menage_db_commit_method,
    CommitMode,
    menage_db_not_found_result_method,
    NotFoundResultMode
)
from wiki.permissions.object.general.models import GeneralDocumentPermission
from wiki.permissions.object.group.models import GroupDocumentPermission
from wiki.permissions.object.individual.models import IndividualDocumentPermission
from wiki.wiki_workspace.document.model import Document
from wiki.wiki_workspace.repository import ObjectRepository


class DocumentRepository(ObjectRepository):
    document_not_found_exception = WikiException(
        message="Document not found.",
        error_code=WikiErrorCode.DOCUMENT_NOT_FOUND,
        http_status_code=status.HTTP_404_NOT_FOUND
    )
    _document_current_commit_already_published_exception = WikiException(
        message="The document in the current version has already been published.",
        error_code=WikiErrorCode.DOCUMENT_CURRENT_COMMIT_ALREADY_PUBLISHED,
        http_status_code=status.HTTP_409_CONFLICT
    )

    async def _get_result_document_with_permission(self, user_id: UUID, *whereclause):
        return await self._get_result_object_with_permission(
            Document,
            IndividualDocumentPermission,
            GroupDocumentPermission,
            GeneralDocumentPermission,
            user_id,
            *whereclause
        )

    async def get_documents_with_permission(self, user_id: UUID) -> list:
        res = await self._get_result_document_with_permission(user_id)
        return res.all()

    @menage_db_not_found_result_method(NotFoundResultMode.EXCEPTION, ex=document_not_found_exception)
    async def get_document_with_permission_by_id(self, user_id: UUID, document_id: UUID):
        res = await self._get_result_document_with_permission(user_id, Document.id == document_id)
        return res.first()

    @menage_db_not_found_result_method(NotFoundResultMode.EXCEPTION, ex=document_not_found_exception)
    async def get_document_by_id(self, document_id: UUID, is_only_existing: bool = True) -> Document:
        whereclause = [Document.id == document_id]
        if is_only_existing:
            whereclause.append(Document.is_deleted == False)

        select_document = select(Document).where(and_(*whereclause))
        document_query = (await self.session.execute(select_document)).scalar()
        return document_query

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

    @menage_db_commit_method(CommitMode.FLUSH)
    async def update_document(self,
                              document: Document,
                              *,
                              title: Optional[str] = None,
                              parent_document: Optional[Document] = None,
                              current_published_version_commit_id: Optional[str] = None):
        if title is not None:
            document.title = title
        if parent_document is not None:
            document.parent_document_id = parent_document.id
        if current_published_version_commit_id is not None:
            if document.current_published_version_commit_id == current_published_version_commit_id:
                raise self._document_current_commit_already_published_exception
            document.current_published_version_commit_id = current_published_version_commit_id

        self.session.add(document)

        return document

    async def get_all_document_with_permission_by_workspace_id(self,
                                                               user_id: UUID,
                                                               workspace_id: UUID,
                                                               is_only_existing: bool = True):
        whereclause = [Document.workspace_id == workspace_id]
        if is_only_existing:
            whereclause.append(Document.is_deleted == False)
        res = await self._get_result_document_with_permission(user_id, *whereclause)
        return res.all()

    async def get_all_document_by_workspace_id(self,
                                               workspace_id: UUID,
                                               is_only_existing: bool = True) -> list[Document]:
        whereclause = [Document.workspace_id == workspace_id]
        if is_only_existing:
            whereclause.append(Document.is_deleted == False)
        document_query = await self.session.execute(select(Document).where(and_(*whereclause)))
        result = document_query.scalars().all()
        return result

    async def get_list_ids_of_document_hierarchy(self, document: Document) -> list[UUID]:
        ids = [document.id]

        while document.parent_document_id is not None:
            document = await self.get_document_by_id(document.parent_document_id)
            ids.append(document.id)

        ids.reverse()

        return ids
