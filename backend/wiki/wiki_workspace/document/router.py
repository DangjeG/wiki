from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from wiki.common.exceptions import WikiException, WikiErrorCode
from wiki.common.schemas import WikiUserHandlerData
from wiki.database.deps import get_db
from wiki.permissions.base import BasePermission
from wiki.user.utils import get_user_info_by_handler_data
from wiki.wiki_api_client.enums import ResponsibilityType
from wiki.wiki_api_client.repository import WikiApiClientRepository
from wiki.wiki_workspace.document.model import Document
from wiki.wiki_workspace.document.repository import DocumentRepository
from wiki.wiki_workspace.document.schemas import CreateDocument, DocumentInfoResponse
from wiki.wiki_workspace.model import Workspace
from wiki.wiki_workspace.repository import WorkspaceRepository

document_router = APIRouter()


@document_router.post(
    "/",
    response_model=DocumentInfoResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Create document if parent_document_id=None then document is in the root."
)
async def create_document(
        new_document: CreateDocument,
        session: AsyncSession = Depends(get_db),
        user: WikiUserHandlerData = Depends(BasePermission(responsibility=ResponsibilityType.VIEWER))
):
    document_repository: DocumentRepository = DocumentRepository(session)
    if new_document.parent_document_id is not None:
        parent_document: Document = await document_repository.get_document_by_id(new_document.parent_document_id)
        if parent_document.workspace_id != new_document.workspace_id:
            raise WikiException(
                message="Document not specified.",
                error_code=WikiErrorCode.WORKSPACE_NOT_SPECIFIED,
                http_status_code=status.HTTP_400_BAD_REQUEST
            )
    workspace_repository: WorkspaceRepository = WorkspaceRepository(session)
    workspace: Workspace = await workspace_repository.get_workspace_by_id(new_document.workspace_id)
    document = await document_repository.create_document(new_document.title,
                                                         new_document.workspace_id,
                                                         user.id,
                                                         new_document.parent_document_id)

    return DocumentInfoResponse(
        id=document.id,
        title=document.title,
        workspace_id=document.workspace_id,
        creator_user=await get_user_info_by_handler_data(user, session),
        parent_document_id=document.parent_document_id
    )


@document_router.get(
    "/",
    response_model=list[DocumentInfoResponse],
    status_code=status.HTTP_200_OK,
    summary="Get all document by workspace id"
)
async def get_documents_by_workspace_id(
        workspace_id: UUID,
        session: AsyncSession = Depends(get_db),
        user: WikiUserHandlerData = Depends(BasePermission(responsibility=ResponsibilityType.VIEWER))
):
    document_repository: DocumentRepository = DocumentRepository(session)
    wiki_api_client_repository: WikiApiClientRepository = WikiApiClientRepository(session)

    documents = await document_repository.get_all_document_by_workspace_id(workspace_id=workspace_id)

    result_documents: list[DocumentInfoResponse] = []
    for doc in documents:
        append_document = DocumentInfoResponse(
            id=doc.id,
            title=doc.title,
            workspace_id=doc.workspace_id,
            creator=await wiki_api_client_repository.get_wiki_api_client_by_id(doc.id),
            parent_document_id=doc.parent_document_id
        )
        result_documents.append(append_document)

    return result_documents
