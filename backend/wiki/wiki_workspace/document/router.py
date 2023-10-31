from uuid import UUID

from fastapi import APIRouter, Depends
from lakefs_client.client import LakeFSClient
from lakefs_client.model.commit import Commit
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from wiki.common.exceptions import WikiException, WikiErrorCode
from wiki.common.schemas import WikiUserHandlerData, BaseResponse
from wiki.database.deps import get_db
from wiki.permissions.base import BasePermission
from wiki.user.models import User
from wiki.user.repository import UserRepository
from wiki.user.utils import get_user_info
from wiki.wiki_api_client.enums import ResponsibilityType
from wiki.wiki_storage.deps import get_storage_client
from wiki.wiki_storage.schemas import CommitMetadataScheme
from wiki.wiki_storage.services.versioning import VersioningWikiStorageService
from wiki.wiki_workspace.document.model import Document
from wiki.wiki_workspace.document.repository import DocumentRepository
from wiki.wiki_workspace.document.schemas import (
    CreateDocument,
    DocumentInfoResponse,
    DocumentNodeInfoResponse
)
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
        creator_user=await get_user_info(user, session, is_full=False),
        parent_document_id=document.parent_document_id
    )


@document_router.post(
    "/{document_id}/save",
    response_model=BaseResponse,
    status_code=status.HTTP_200_OK,
    summary="Saving document",
    description="## Saving document\nCommits changes, a new version will be created for all changed objects"
)
async def save_document(
        document_id: UUID,
        session: AsyncSession = Depends(get_db),
        storage_client: LakeFSClient = Depends(get_storage_client),
        user: WikiUserHandlerData = Depends(BasePermission(responsibility=ResponsibilityType.VIEWER))
):
    document_repository: DocumentRepository = DocumentRepository(session)
    document = await document_repository.get_document_by_id(document_id)
    user_repository: UserRepository = UserRepository(session)
    user_db: User = await user_repository.get_user_by_id(user.id)

    storage_service: VersioningWikiStorageService = VersioningWikiStorageService(storage_client)
    resp: Commit = storage_service.commit_workspace_version(document.workspace_id,
                                                            CommitMetadataScheme(committer_user_id=str(user_db.id)))

    return BaseResponse(msg="Document saved")


@document_router.get(
    "/all",
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
    documents = await document_repository.get_all_document_by_workspace_id(workspace_id=workspace_id)
    user_repository: UserRepository = UserRepository(session)

    result_documents: list[DocumentInfoResponse] = []
    for doc in documents:
        user_db = await user_repository.get_user_by_id(doc.creator_user_id)
        append_document = DocumentInfoResponse(
            id=doc.id,
            title=doc.title,
            workspace_id=doc.workspace_id,
            creator_user=await get_user_info(user_db, session, is_full=False),
            parent_document_id=doc.parent_document_id
        )
        result_documents.append(append_document)

    return result_documents


@document_router.get(
    "/info",
    response_model=DocumentInfoResponse,
    status_code=status.HTTP_200_OK,
    summary="Get document info by id"
)
async def get_document_info_by_id(
        document_id: UUID,
        session: AsyncSession = Depends(get_db),
        user: WikiUserHandlerData = Depends(BasePermission(responsibility=ResponsibilityType.VIEWER))
):
    document_repository: DocumentRepository = DocumentRepository(session)
    document = await document_repository.get_document_by_id(document_id)

    return DocumentInfoResponse(
        id=document.id,
        title=document.title,
        workspace_id=document.workspace_id,
        creator_user=await get_user_info(document.creator_user_id, session, False),
        parent_document_id=document.parent_document_id
    )


@document_router.get(
    "/tree",
    response_model=list[DocumentNodeInfoResponse],
    status_code=status.HTTP_200_OK,
    summary="Get all tree document by workspace id"
)
async def get_tree_documents_by_workspace_id(
        workspace_id: UUID,
        session: AsyncSession = Depends(get_db),
        user: WikiUserHandlerData = Depends(BasePermission(responsibility=ResponsibilityType.VIEWER))
):
    document_repository: DocumentRepository = DocumentRepository(session)
    documents = await document_repository.get_all_document_by_workspace_id(workspace_id)
    result_docs: list[DocumentNodeInfoResponse] = get_children_document(documents)

    return result_docs


def get_children_document(documents: list[Document], document_id: UUID = None) -> list[DocumentNodeInfoResponse]:
    result_docs: list[DocumentNodeInfoResponse] = []
    for doc in documents:
        if doc.parent_document_id == document_id:
            new_doc = DocumentNodeInfoResponse(
                id=doc.id,
                title=doc.title
            )
            result_docs.append(new_doc)
            children = get_children_document(documents, doc.id)
            if len(children) > 0:
                new_doc.children = children

    return result_docs
