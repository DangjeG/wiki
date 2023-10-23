from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from wiki.database.deps import get_db
from wiki.wiki_api_client.repository import WikiApiClientRepository
from wiki.wiki_workspace.document.repository import DocumentRepository
from wiki.wiki_workspace.document.schemas import DocumentResponse, CreateDocument, DocumentInfo

document_router = APIRouter()

@document_router.post(
    "/document",
    response_model=DocumentResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Create document if parent_document_id=None then document is in the root."
)
async def create_document(
        new_document: CreateDocument,
        session: AsyncSession = Depends(get_db)
):
    document_repository: DocumentRepository = DocumentRepository(session)

    await document_repository.create_document(new_document)

    return DocumentResponse(
        title=new_document.title
    )

@document_router.get(
    "/document",
    response_model=list[DocumentInfo],
    status_code=status.HTTP_202_ACCEPTED,
    summary="Get all document by workspace id"
)
async def get_documents_by_workspace_id(
        workspace_id: UUID,
        session: AsyncSession = Depends(get_db)
):
    document_repository: DocumentRepository = DocumentRepository(session)
    wiki_api_client_repository: WikiApiClientRepository = WikiApiClientRepository(session)

    documents = await document_repository.get_all_document_by_workspace_id(workspace_id=workspace_id)

    result_documents: list[DocumentInfo] = []
    for doc in documents:
        append_document = DocumentInfo(
            title=doc.title,
            workspace_id=doc.workspace_id,
            creator=await wiki_api_client_repository.get_wiki_api_client_by_id(doc.id),
            parent_document_id=doc.parent_document_id
        )
        result_documents.append(append_document)

    return result_documents
