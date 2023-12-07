from io import StringIO
from typing import Optional
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
from wiki.permissions.object.enums import ObjectPermissionMode
from wiki.permissions.object.transporter import PermissionTransporter
from wiki.permissions.object.utils import get_permission_mode_by_responsibility
from wiki.user.models import User
from wiki.user.repository import UserRepository
from wiki.user.utils import get_user_info
from wiki.wiki_api_client.enums import ResponsibilityType
from wiki.wiki_storage.deps import get_storage_client
from wiki.wiki_storage.schemas import CommitMetadataScheme
from wiki.wiki_storage.services.versioning import VersioningWikiStorageService
from wiki.wiki_workspace.block.repository import BlockRepository
from wiki.wiki_workspace.block.schemas import CreateBlock
from wiki.wiki_workspace.block.templates import get_template_first_block
from wiki.wiki_workspace.document.model import Document
from wiki.wiki_workspace.document.repository import DocumentRepository
from wiki.wiki_workspace.document.schemas import (
    CreateDocument,
    DocumentInfoResponse,
    DocumentNodeInfoResponse
)
from wiki.wiki_workspace.document_template.model import DocumentTemplate
from wiki.wiki_workspace.document_template.repository import DocumentTemplateRepository
from wiki.wiki_workspace.repository import WorkspaceRepository


document_router = APIRouter()


@document_router.post(
    "/",
    response_model=DocumentInfoResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Create document"
)
async def create_document(
        new_document: CreateDocument,
        template_id: UUID = None,
        session: AsyncSession = Depends(get_db),
        storage_client: LakeFSClient = Depends(get_storage_client),
        user: WikiUserHandlerData = Depends(BasePermission(responsibility=ResponsibilityType.VIEWER))
):
    """
    ## Create document
    Create a document using a template,
    if template_id=None then will be created empty document,
    if parent_document_id=None then document is in the root.
    """

    user_repository: UserRepository = UserRepository(session)
    user_db: User = await user_repository.get_user_by_id(user.id)
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
    workspace = await workspace_repository.get_workspace_with_permission_by_id(user.id, new_document.workspace_id)

    if (not user.wiki_api_client.responsibility == ResponsibilityType.ADMIN and
            ObjectPermissionMode(workspace.permission_mode) < ObjectPermissionMode.EDITING):
        raise WikiException(
            message="You can't create documents in this workspace. You must have permission to edit the workspace to create a document.",
            error_code=WikiErrorCode.DOCUMENT_CREATE_FORBIDDEN,
            http_status_code=status.HTTP_403_FORBIDDEN
        )

    document = await document_repository.create_document(new_document.title,
                                                         new_document.workspace_id,
                                                         user_db.id,
                                                         new_document.parent_document_id)

    permission_transporter = PermissionTransporter(session)
    await permission_transporter.transfer_to_document(document, workspace)

    storage_service: VersioningWikiStorageService = VersioningWikiStorageService(storage_client)
    storage_service.create_branch_for_workspace_document(workspace.id, document.id)

    # You must create at least one block to create the first starting publication of a document
    block_repository: BlockRepository = BlockRepository(session)
    new_blocks = []
    if template_id is None:
        block = await block_repository.create_block(get_template_first_block(document.id))
        await permission_transporter.transfer_to_block(block, document)
        document_ids = await document_repository.get_list_ids_of_document_hierarchy(document)
        storage_service.upload_document_block_in_workspace_storage(content=StringIO(""),
                                                                   workspace_id=document.workspace_id,
                                                                   document_ids=document_ids,
                                                                   block_id=block.id)

        new_blocks.append(block)
    else:
        document_template_repository: DocumentTemplateRepository = DocumentTemplateRepository(session)
        template: DocumentTemplate = await document_template_repository.get_document_template_by_id(template_id)
        document_template = await document_repository.get_document_by_id(document_id=template.document_id, is_only_existing=False)
        template_blocks = await block_repository.get_all_block_by_document_id(document_template.id)
        for template_block in template_blocks:
            block = await block_repository.create_block(CreateBlock(
                    document_id=document.id,
                    position=template_block.position,
                    type_block=template_block.type_block
                ))
            new_blocks.append(block)

            await permission_transporter.transfer_to_block(block, document)
            document_template_ids = await document_repository.get_list_ids_of_document_hierarchy(document_template)
            content = storage_service.get_content_document_block_in_workspace_storage(
                workspace_id=document_template.workspace_id,
                document_ids=document_template_ids,
                block_id=template_block.id,
                version_commit_id=template.orig_commit_id
            )
            document_ids = await document_repository.get_list_ids_of_document_hierarchy(document)
            storage_service.upload_document_block_in_workspace_storage(
                content=StringIO(content),
                workspace_id=document.workspace_id,
                document_ids=document_ids,
                block_id=block.id
            )

    # Commit the starting block
    resp: Commit = storage_service.commit_workspace_document_version(document.workspace_id,
                                                                     document.id,
                                                                     CommitMetadataScheme(
                                                                         committer_user_id=str(user_db.id)))
    for block in new_blocks:
        await block_repository.create_version_block(block, resp.id)

    # Immediately publish a blank version of the document
    await _publish_document(document, document_repository, storage_service)

    document = await document_repository.get_document_with_permission_by_id(user.id, document.id)

    return DocumentInfoResponse(
        id=document.id,
        title=document.title,
        workspace_id=document.workspace_id,
        creator_user=await get_user_info(user, session, is_full=False),
        parent_document_id=document.parent_document_id,
        created_at=document.created_at,
        last_published_version_at=document.last_published_version_at,
        permission_mode=get_permission_mode_by_responsibility(
            document.permission_mode,
            user.wiki_api_client.responsibility
        )
    )


@document_router.post(
    "/{document_id}/publish",
    response_model=BaseResponse,
    status_code=status.HTTP_200_OK,
    summary="Publish document"
)
async def publish_document(
        document_id: UUID,
        is_save_last_uncommitted_changes: bool = True,
        session: AsyncSession = Depends(get_db),
        storage_client: LakeFSClient = Depends(get_storage_client),
        user: WikiUserHandlerData = Depends(BasePermission(responsibility=ResponsibilityType.VIEWER))
):
    """
    ## Publish document

    The last committed (saved) version of the document will be published and available for viewing according to the set permissions.

    :param document_id: The identifier of the document you are publishing.
    :param is_save_last_uncommitted_changes: If set to true, all uncommitted changes (user did not send a save request) will be automatically saved.
    """
    document_repository: DocumentRepository = DocumentRepository(session)
    document = await document_repository.get_document_with_permission_by_id(user.id, document_id)
    if (not user.wiki_api_client.responsibility == ResponsibilityType.ADMIN and
            ObjectPermissionMode(document.permission_mode) < ObjectPermissionMode.EDITING):
        raise WikiException(
            message="You can't publish this document. You must have permission to edit it.",
            error_code=WikiErrorCode.DOCUMENT_PUBLISH_FORBIDDEN,
            http_status_code=status.HTTP_403_FORBIDDEN
        )

    user_repository: UserRepository = UserRepository(session)
    user_db: User = await user_repository.get_user_by_id(user.id)

    storage_service: VersioningWikiStorageService = VersioningWikiStorageService(storage_client)
    if is_save_last_uncommitted_changes:
        try:
            resp: Commit = storage_service.commit_workspace_document_version(document.workspace_id,
                                                                             document.id,
                                                                             CommitMetadataScheme(
                                                                                 committer_user_id=str(user_db.id)))
            block_repository = BlockRepository(session)
            blocks = await block_repository.get_all_block_by_document_id(document.id)
            for block in blocks:
                await block_repository.create_version_block(block, resp.id)
        except WikiException:
            pass

    document = await document_repository.get_document_by_id(document_id)
    await _publish_document(document, document_repository, storage_service)

    return BaseResponse(msg="Document published")


async def _publish_document(document: Document,
                            document_repository: DocumentRepository,
                            storage_service: VersioningWikiStorageService):
    document_ids = await document_repository.get_list_ids_of_document_hierarchy(document)
    res: dict = storage_service.get_current_version_document_commit_id(document.workspace_id, document_ids)
    commit_id = res.get("commit_id")
    if commit_id is None:
        raise storage_service.commits_not_found_exception
    await document_repository.update_document(document, current_published_version_commit_id=commit_id)


@document_router.post(
    "/{document_id}/save",
    response_model=BaseResponse,
    status_code=status.HTTP_200_OK,
    summary="Saving document"
)
async def save_document(
        document_id: UUID,
        session: AsyncSession = Depends(get_db),
        storage_client: LakeFSClient = Depends(get_storage_client),
        user: WikiUserHandlerData = Depends(BasePermission(responsibility=ResponsibilityType.VIEWER))
):
    """
    ## Saving document

    Commits changes, a new version will be created for all changed document objects.
    """
    document_repository: DocumentRepository = DocumentRepository(session)
    document = await document_repository.get_document_with_permission_by_id(user.id, document_id)

    if (not user.wiki_api_client.responsibility == ResponsibilityType.ADMIN and
            ObjectPermissionMode(document.permission_mode) < ObjectPermissionMode.EDITING):
        raise WikiException(
            message="You can't save this document. You must have permission to edit it.",
            error_code=WikiErrorCode.DOCUMENT_SAVE_FORBIDDEN,
            http_status_code=status.HTTP_403_FORBIDDEN
        )

    user_repository: UserRepository = UserRepository(session)
    user_db: User = await user_repository.get_user_by_id(user.id)

    storage_service: VersioningWikiStorageService = VersioningWikiStorageService(storage_client)
    resp: Commit = storage_service.commit_workspace_document_version(document.workspace_id,
                                                                     document.id,
                                                                     CommitMetadataScheme(committer_user_id=str(user_db.id)))
    block_repository = BlockRepository(session)
    blocks = await block_repository.get_all_block_by_document_id(document.id)
    for block in blocks:
        await block_repository.create_version_block(block, resp.id)

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
    documents = await document_repository.get_all_document_with_permission_by_workspace_id(
        user.id,
        workspace_id
    )
    user_repository: UserRepository = UserRepository(session)

    result_documents: list[DocumentInfoResponse] = []
    for doc in documents:
        if (user.wiki_api_client.responsibility == ResponsibilityType.ADMIN or
                ObjectPermissionMode(doc.permission_mode) > ObjectPermissionMode.HIDDEN_INACCESSIBLE):
            append_document = DocumentInfoResponse(
                id=doc.id,
                title=doc.title,
                workspace_id=doc.workspace_id,
                creator_user=await get_user_info(doc.creator_user_id, session, is_full=False),
                parent_document_id=doc.parent_document_id,
                created_at=doc.created_at,
                last_published_version_at=doc.last_published_version_at,
                permission_mode=get_permission_mode_by_responsibility(
                    doc.permission_mode,
                    user.wiki_api_client.responsibility
                )
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
    document = await document_repository.get_document_with_permission_by_id(user.id, document_id)

    if (user.wiki_api_client.responsibility == ResponsibilityType.ADMIN or
            ObjectPermissionMode(document.permission_mode) > ObjectPermissionMode.HIDDEN_INACCESSIBLE):
        return DocumentInfoResponse(
            id=document.id,
            title=document.title,
            workspace_id=document.workspace_id,
            creator_user=await get_user_info(document.creator_user_id, session, False),
            parent_document_id=document.parent_document_id,
            created_at=document.created_at,
            last_published_version_at=document.last_published_version_at,
            permission_mode=get_permission_mode_by_responsibility(
                document.permission_mode,
                user.wiki_api_client.responsibility
            )
        )
    else:
        raise document_repository.document_not_found_exception


@document_router.get(
    "/tree",
    response_model=list[DocumentNodeInfoResponse],
    status_code=status.HTTP_200_OK,
    summary="Get tree documents"
)
async def get_tree_documents_by_workspace_id(
        workspace_id: UUID,
        max_deep: Optional[int] = 0,
        root_document_id: Optional[UUID] = None,
        session: AsyncSession = Depends(get_db),
        user: WikiUserHandlerData = Depends(BasePermission(responsibility=ResponsibilityType.VIEWER))
):
    """
    ## Get tree documents from workspace
    Get all tree document by workspace id
    If root_document_id=None then be the root workspace
    If max_deep=None or root_document_id=0 then will be returned all document


    !!! Hiding a document (HIDDEN_INACCESSIBLE) from the user at the top
    of the hierarchy will also hide documents lower down the hierarchy
    """

    document_repository: DocumentRepository = DocumentRepository(session)
    documents = await document_repository.get_all_document_with_permission_by_workspace_id(user.id, workspace_id)
    result_docs: list[DocumentNodeInfoResponse] = get_children_document(
        documents=documents,
        root_document_id=root_document_id,
        max_deep=max_deep,
        user=user
    )

    return result_docs


def get_children_document(documents: list[Document],
                          user: WikiUserHandlerData,
                          root_document_id: UUID = None,
                          max_deep: int = None,
                          current_deep: int = 0) -> list[DocumentNodeInfoResponse]:
    """
    !!! Hiding a document (HIDDEN_INACCESSIBLE) from the user at the top
    of the hierarchy will also hide documents lower down the hierarchy
    """

    result_docs: list[DocumentNodeInfoResponse] = []
    for doc in documents:
        if doc.parent_document_id == root_document_id:
            new_doc = DocumentNodeInfoResponse(
                id=doc.id,
                title=doc.title,
                last_published_version_at=doc.last_published_version_at,
                permission_mode=get_permission_mode_by_responsibility(
                    doc.permission_mode,
                    user.wiki_api_client.responsibility
                )
            )
            if (user.wiki_api_client.responsibility == ResponsibilityType.ADMIN or
                    ObjectPermissionMode(doc.permission_mode) > ObjectPermissionMode.HIDDEN_INACCESSIBLE):
                result_docs.append(new_doc)
            current_deep += 1
            if max_deep == 0 or current_deep < max_deep:
                children = get_children_document(
                    documents=documents,
                    root_document_id=doc.id,
                    max_deep=max_deep,
                    current_deep=current_deep,
                    user=user
                )
                if len(children) > 0:
                    new_doc.is_have_children = True
                current_deep -= 1
                if len(children) > 0:
                    new_doc.children = children

    return result_docs
