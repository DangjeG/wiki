from io import StringIO
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, UploadFile, File
from lakefs_client.client import LakeFSClient
from pydantic import constr
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from yadisk_async import YaDisk

from wiki.asset.enums import AssetType
from wiki.asset.model import Asset
from wiki.asset.repository import AssetRepository
from wiki.assets_storage.deps import get_ya_disk_session_storage
from wiki.assets_storage.services.yadisk import YaDiskAssetsStorage
from wiki.common.exceptions import WikiException, WikiErrorCode
from wiki.common.schemas import WikiUserHandlerData, BaseResponse
from wiki.config import settings
from wiki.database.deps import get_db
from wiki.permissions.base import BasePermission
from wiki.permissions.object.enums import ObjectPermissionMode
from wiki.permissions.object.transporter import PermissionTransporter
from wiki.permissions.object.utils import get_permission_mode_by_responsibility
from wiki.wiki_api_client.enums import ResponsibilityType
from wiki.wiki_storage.deps import get_storage_client
from wiki.wiki_storage.services.base import BaseWikiStorageService
from wiki.wiki_workspace.block.model import TypeBlock
from wiki.wiki_workspace.block.repository import BlockRepository
from wiki.wiki_workspace.block.schemas import (
    CreateBlock,
    BlockDataResponse,
    UpdateBlockData,
    UpdateBlockInfo,
    BlockInfoResponse,
    WikiLinkSchema
)
from wiki.wiki_workspace.common import get_block_data_by_id, get_data_blocks
from wiki.wiki_workspace.document.repository import DocumentRepository
from wiki.wiki_workspace.model import Workspace
from wiki.wiki_workspace.repository import WorkspaceRepository


block_router = APIRouter()


@block_router.post(
    "/",
    response_model=BlockDataResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Create block"
)
async def create_block(
        new_block: CreateBlock,
        session: AsyncSession = Depends(get_db),
        storage_client: LakeFSClient = Depends(get_storage_client),
        user: WikiUserHandlerData = Depends(BasePermission(responsibility=ResponsibilityType.VIEWER))
):
    document_repository: DocumentRepository = DocumentRepository(session)
    document = await document_repository.get_document_with_permission_by_id(user.id, new_block.document_id)

    if (not user.wiki_api_client.responsibility == ResponsibilityType.ADMIN and
            ObjectPermissionMode(document.permission_mode) < ObjectPermissionMode.EDITING):
        raise WikiException(
            message="You can't create block in this document. You must have permission to edit the document to create a block.",
            error_code=WikiErrorCode.BLOCK_CREATE_FORBIDDEN,
            http_status_code=status.HTTP_403_FORBIDDEN
        )

    document_ids = await document_repository.get_list_ids_of_document_hierarchy(document)

    block_repository: BlockRepository = BlockRepository(session)
    permission_transporter = PermissionTransporter(session)
    block = await block_repository.create_block(new_block)
    await permission_transporter.transfer_to_block(block, document)
    block = await block_repository.get_block_with_permission_by_id(user.id, block.id)

    storage_service: BaseWikiStorageService = BaseWikiStorageService(storage_client)
    storage_service.upload_document_block_in_workspace_storage(content=StringIO(""),
                                                               workspace_id=document.workspace_id,
                                                               document_ids=document_ids,
                                                               block_id=block.id)
    return BlockDataResponse(
        id=block.id,
        position=block.position,
        document_id=document.id,
        type_block=block.type_block,
        content=StringIO("").getvalue(),
        created_at=block.created_at,
        permission_mode=get_permission_mode_by_responsibility(
            block.permission_mode,
            user.wiki_api_client.responsibility
        )
    )


_update_block_forbidden_exception = WikiException(
    message="You can't update this block. You must have permission to edit it.",
    error_code=WikiErrorCode.BLOCK_UPDATE_FORBIDDEN,
    http_status_code=status.HTTP_403_FORBIDDEN
)


@block_router.put(
    "/data/link",
    response_model=BlockDataResponse,
    status_code=status.HTTP_200_OK,
    summary="Update wiki link data document block"
)
async def update_block_data_link(
        block_id: UUID,
        update_link: WikiLinkSchema,
        session: AsyncSession = Depends(get_db),
        storage_client: LakeFSClient = Depends(get_storage_client),
        user: WikiUserHandlerData = Depends(BasePermission(responsibility=ResponsibilityType.VIEWER))
):
    """
    ## Update wiki link data document block
    One of the specified object ids will be used to create the link in priority: block_id, document_id, workspace_id
    """

    block_repository: BlockRepository = BlockRepository(session)
    block = await block_repository.get_block_with_permission_by_id(user.id, block_id)

    if (not user.wiki_api_client.responsibility == ResponsibilityType.ADMIN and
            ObjectPermissionMode(block.permission_mode) < ObjectPermissionMode.EDITING):
        raise _update_block_forbidden_exception

    if TypeBlock(block.type_block) != TypeBlock.WIKI_LINK:
        raise WikiException(
            message="Doesn't match block type.",
            error_code=WikiErrorCode.BLOCK_NOT_SPECIFIED,
            http_status_code=status.HTTP_409_CONFLICT
        )

    document_repository: DocumentRepository = DocumentRepository(session)
    document = await document_repository.get_document_by_id(block.document_id)
    document_ids = await document_repository.get_list_ids_of_document_hierarchy(document)
    workspace_repository: WorkspaceRepository = WorkspaceRepository(session)
    workspace: Workspace = await workspace_repository.get_workspace_by_id(document.workspace_id)

    if list(update_link.model_dump().values()).count(None) != len(update_link.model_fields) - 1:
        raise WikiException(
            message="It is necessary to specify at least one object id for link creation",
            error_code=WikiErrorCode.BLOCK_NOT_SPECIFIED,
            http_status_code=status.HTTP_400_BAD_REQUEST
        )

    content = update_link.to_content_string()
    storage_service: BaseWikiStorageService = BaseWikiStorageService(storage_client)
    storage_service.upload_document_block_in_workspace_storage(content=StringIO(content),
                                                               workspace_id=workspace.id,
                                                               document_ids=document_ids,
                                                               block_id=block.id)

    return BlockDataResponse(
        id=block.id,
        document_id=block.document_id,
        position=block.position,
        type_block=block.type_block,
        content=update_link,
        created_at=block.created_at,
        permission_mode=get_permission_mode_by_responsibility(
            block.permission_mode,
            user.wiki_api_client.responsibility
        )
    )


@block_router.put(
    "/data/file",
    response_model=BlockDataResponse,
    status_code=status.HTTP_200_OK,
    summary="Update file data document block"
)
async def update_block_data_file(
        block_id: UUID,
        file: UploadFile = File(),
        session: AsyncSession = Depends(get_db),
        ya_disk: YaDisk = Depends(get_ya_disk_session_storage),
        storage_client: LakeFSClient = Depends(get_storage_client),
        user: WikiUserHandlerData = Depends(BasePermission(responsibility=ResponsibilityType.VIEWER))
):
    block_repository: BlockRepository = BlockRepository(session)
    block = await block_repository.get_block_with_permission_by_id(user.id, block_id)

    if (not user.wiki_api_client.responsibility == ResponsibilityType.ADMIN and
            ObjectPermissionMode(block.permission_mode) < ObjectPermissionMode.EDITING):
        raise _update_block_forbidden_exception

    if TypeBlock(block.type_block) in [TypeBlock.TEXT, TypeBlock.WIKI_LINK]:
        raise WikiException(
            message="Doesn't match block type.",
            error_code=WikiErrorCode.BLOCK_NOT_SPECIFIED,
            http_status_code=status.HTTP_409_CONFLICT
        )
    document_repository: DocumentRepository = DocumentRepository(session)
    document = await document_repository.get_document_by_id(block.document_id)
    document_ids = await document_repository.get_list_ids_of_document_hierarchy(document)
    workspace_repository: WorkspaceRepository = WorkspaceRepository(session)
    workspace: Workspace = await workspace_repository.get_workspace_by_id(document.workspace_id)

    if file.size / 1024 > settings.ASSET_SIZE_LIMIT_KB:
        raise WikiException(
            message=f"Limit {settings.ASSET_SIZE_LIMIT_KB} KB the size of the downloaded asset has been exceeded.",
            error_code=WikiErrorCode.ASSET_LIMIT_SIZE_EXCEEDED_EXCEPTION,
            http_status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
        )

    asset_repository = AssetRepository(session)
    asset_type = AssetType.DOCUMENT
    if TypeBlock(block.type_block) == TypeBlock.IMG:
        asset_type = AssetType.IMAGE

    asset: Asset = await asset_repository.create_asset(
        asset_type=asset_type,
        name=file.filename,
        size_kb=file.size / 1024,
        uploader_user_id=user.id,
        workspace_id=workspace.id
    )

    ya_storage = YaDiskAssetsStorage(ya_disk)
    await ya_storage.upload_asset(asset, file.file)

    content = str(asset.id)
    storage_service: BaseWikiStorageService = BaseWikiStorageService(storage_client)
    storage_service.upload_document_block_in_workspace_storage(content=StringIO(content),
                                                               workspace_id=workspace.id,
                                                               document_ids=document_ids,
                                                               block_id=block.id)

    return BlockDataResponse(
        id=block.id,
        document_id=block.document_id,
        position=block.position,
        type_block=block.type_block,
        content=content,
        created_at=block.created_at,
        link=await ya_storage.download_asset(asset),
        permission_mode=get_permission_mode_by_responsibility(
            block.permission_mode,
            user.wiki_api_client.responsibility
        )
    )


@block_router.put(
    "/data/text",
    response_model=BlockDataResponse,
    status_code=status.HTTP_200_OK,
    summary="Update text data document block"
)
async def update_block_data_text(
        update_data_block: UpdateBlockData,
        session: AsyncSession = Depends(get_db),
        storage_client: LakeFSClient = Depends(get_storage_client),
        user: WikiUserHandlerData = Depends(BasePermission(responsibility=ResponsibilityType.VIEWER))
):
    block_repository: BlockRepository = BlockRepository(session)
    block = await block_repository.get_block_with_permission_by_id(user.id, update_data_block.block_id)

    if (not user.wiki_api_client.responsibility == ResponsibilityType.ADMIN and
            ObjectPermissionMode(block.permission_mode) < ObjectPermissionMode.EDITING):
        raise _update_block_forbidden_exception

    if TypeBlock(block.type_block) != TypeBlock.TEXT:
        raise WikiException(
            message="Doesn't match block type.",
            error_code=WikiErrorCode.BLOCK_NOT_SPECIFIED,
            http_status_code=status.HTTP_409_CONFLICT
        )
    document_repository: DocumentRepository = DocumentRepository(session)
    document = await document_repository.get_document_by_id(block.document_id)
    document_ids = await document_repository.get_list_ids_of_document_hierarchy(document)
    workspace_repository: WorkspaceRepository = WorkspaceRepository(session)
    workspace: Workspace = await workspace_repository.get_workspace_by_id(document.workspace_id)

    storage_service: BaseWikiStorageService = BaseWikiStorageService(storage_client)
    storage_service.upload_document_block_in_workspace_storage(content=StringIO(update_data_block.content),
                                                               workspace_id=workspace.id,
                                                               document_ids=document_ids,
                                                               block_id=block.id)

    return BlockDataResponse(
        id=block.id,
        document_id=block.document_id,
        position=block.position,
        type_block=block.type_block,
        content=update_data_block.content,
        created_at=block.created_at,
        permission_mode=get_permission_mode_by_responsibility(
            block.permission_mode,
            user.wiki_api_client.responsibility
        )
    )


@block_router.put(
    "/info",
    response_model=BlockInfoResponse,
    status_code=status.HTTP_200_OK,
    summary="Update info document block"
)
async def update_block_info(
        update_data_block: UpdateBlockInfo,
        session: AsyncSession = Depends(get_db),
        user: WikiUserHandlerData = Depends(BasePermission(responsibility=ResponsibilityType.VIEWER))
):
    block_repository: BlockRepository = BlockRepository(session)
    block_perm = await block_repository.get_block_with_permission_by_id(user.id, update_data_block.block_id)

    if (not user.wiki_api_client.responsibility == ResponsibilityType.ADMIN and
            ObjectPermissionMode(block_perm.permission_mode) < ObjectPermissionMode.EDITING):
        raise _update_block_forbidden_exception

    block = await block_repository.update_block(update_data_block.block_id,
                                                position=update_data_block.position,
                                                type_block=update_data_block.type_block)

    return BlockInfoResponse(
        id=block.id,
        document_id=block.document_id,
        position=block.position,
        type_block=block.type_block,
        created_at=block.created_at,
        permission_mode=get_permission_mode_by_responsibility(
            block_perm.permission_mode,
            user.wiki_api_client.responsibility
        )
    )


@block_router.delete(
    "/",
    response_model=BaseResponse,
    status_code=status.HTTP_200_OK,
    summary="Delete a block from a document"
)
async def delete_block(
        block_id: UUID,
        session: AsyncSession = Depends(get_db),
        user: WikiUserHandlerData = Depends(BasePermission(responsibility=ResponsibilityType.VIEWER))
):
    block_repository: BlockRepository = BlockRepository(session)
    block_perm = await block_repository.get_block_with_permission_by_id(user.id, block_id)

    if (not user.wiki_api_client.responsibility == ResponsibilityType.ADMIN and
            ObjectPermissionMode(block_perm.permission_mode) < ObjectPermissionMode.DELETION):
        raise _update_block_forbidden_exception

    await block_repository.mark_block_deleted(block_id)

    return BaseResponse(
        msg="The document block has been deleted."
    )


@block_router.get(
    "/data/all",
    response_model=list[BlockDataResponse],
    status_code=status.HTTP_200_OK,
    summary="Get all data blocks by id document"
)
async def get_blocks(
        document_id: UUID,
        session: AsyncSession = Depends(get_db),
        storage_client: LakeFSClient = Depends(get_storage_client),
        ya_disk: YaDisk = Depends(get_ya_disk_session_storage),
        version_commit_id: Optional[constr(min_length=64, max_length=64)] = None,
        user: WikiUserHandlerData = Depends(BasePermission(responsibility=ResponsibilityType.VIEWER))
):
    """
    ## Getting document blocks data

    :param document_id: Document Identifier
    :param version_commit_id: Specify the commit identifier of a particular version. If None, get the latest version of the data.
    """

    document_repo = DocumentRepository(session)
    document = await document_repo.get_document_with_permission_by_id(user.id, document_id)
    if (not user.wiki_api_client.responsibility == ResponsibilityType.ADMIN and
            ObjectPermissionMode(document.permission_mode) < ObjectPermissionMode.EDITING):
        raise WikiException(
            message="You can't get data this block. To perform this operation, you must have permission"
                    "to perform document editing. If you have permission to view, use: /publish/data.",
            error_code=WikiErrorCode.DOCUMENT_SAVE_FORBIDDEN,
            http_status_code=status.HTTP_403_FORBIDDEN
        )

    res = await get_data_blocks(session, user, document_id, version_commit_id, storage_client)
    ya_storage = YaDiskAssetsStorage(ya_disk)
    asset_repository = AssetRepository(session)
    return await set_asset_link_for_block(res, asset_repository, ya_storage)


@block_router.get(
    "/data",
    response_model=BlockDataResponse,
    status_code=status.HTTP_200_OK,
    summary="Get data block by id"
)
async def get_block_by_id(
        block_id: UUID,
        version_commit_id: Optional[constr(min_length=64, max_length=64)] = None,
        session: AsyncSession = Depends(get_db),
        storage_client: LakeFSClient = Depends(get_storage_client),
        ya_disk: YaDisk = Depends(get_ya_disk_session_storage),
        user: WikiUserHandlerData = Depends(BasePermission(responsibility=ResponsibilityType.VIEWER))
):

    block: BlockDataResponse = await get_block_data_by_id(session,
                                                          user,
                                                          block_id,
                                                          storage_client,
                                                          version_commit_id)
    ya_storage = YaDiskAssetsStorage(ya_disk)
    asset_repository = AssetRepository(session)
    res = await set_asset_link_for_block([block], asset_repository, ya_storage)

    return res[0]


@block_router.get(
    "/publish/data",
    response_model=list[BlockDataResponse],
    status_code=status.HTTP_200_OK,
    summary="Get all publish data blocks by id document"
)
async def get_publish_blocks(
        document_id: UUID,
        session: AsyncSession = Depends(get_db),
        storage_client: LakeFSClient = Depends(get_storage_client),
        ya_disk: YaDisk = Depends(get_ya_disk_session_storage),
        user: WikiUserHandlerData = Depends(BasePermission(responsibility=ResponsibilityType.VIEWER))
):
    """
    ## Getting published document blocks data
    """

    document_repository: DocumentRepository = DocumentRepository(session)
    document = await document_repository.get_document_by_id(document_id)

    if (not user.wiki_api_client.responsibility == ResponsibilityType.ADMIN and
            ObjectPermissionMode(document.permission_mode) < ObjectPermissionMode.VIEW_AND_EXPORT):
        raise WikiException(
            message="You aren't to view this document. You must have permission to view and export it.",
            error_code=WikiErrorCode.DOCUMENT_VIEW_FORBIDDEN,
            http_status_code=status.HTTP_403_FORBIDDEN
        )

    res = await get_data_blocks(session,
                                user,
                                document_id,
                                document.current_published_version_commit_id,
                                storage_client)
    ya_storage = YaDiskAssetsStorage(ya_disk)
    asset_repository = AssetRepository(session)
    return await set_asset_link_for_block(res, asset_repository, ya_storage)


async def set_asset_link_for_block(data: list[BlockDataResponse],
                                   asset_repository: AssetRepository,
                                   ya_storage: YaDiskAssetsStorage):
    for r in data:
        if (not r.type_block in (TypeBlock.TEXT, TypeBlock.WIKI_LINK) and
                r.content != "" and
                r.permission_mode > ObjectPermissionMode.INACCESSIBLE):
            asset = await asset_repository.get_asset_by_id(UUID(r.content))
            r.link = await ya_storage.download_asset(asset)

    return data
