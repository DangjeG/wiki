from uuid import UUID

from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from yadisk_async import YaDisk

from wiki.asset.enums import AssetType
from wiki.asset.model import Asset
from wiki.asset.repository import AssetRepository
from wiki.asset.schema import AssetInfoResponse, UpdateAsset
from wiki.assets_storage.deps import get_ya_disk_session_storage
from wiki.assets_storage.services.yadisk import YaDiskAssetsStorage
from wiki.common.exceptions import WikiException, WikiErrorCode
from wiki.common.schemas import WikiUserHandlerData, BaseResponse
from wiki.config import settings
from wiki.database.deps import get_db
from wiki.permissions.base import BasePermission
from wiki.user.models import User
from wiki.user.repository import UserRepository
from wiki.user.utils import get_user_info
from wiki.wiki_api_client.enums import ResponsibilityType
from wiki.wiki_workspace.model import Workspace
from wiki.wiki_workspace.repository import WorkspaceRepository
from wiki.wiki_workspace.utils import get_workspace_info


asset_storage_router = APIRouter()


@asset_storage_router.post(
    "/asset/upload",
    response_model=AssetInfoResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Upload Asset"
)
async def create_and_upload_asset(
        workspace_id: UUID,
        asset_type: AssetType,
        file: UploadFile = File(),
        session: AsyncSession = Depends(get_db),
        ya_disk: YaDisk = Depends(get_ya_disk_session_storage),
        user: WikiUserHandlerData = Depends(BasePermission(responsibility=ResponsibilityType.VIEWER))
):
    if file.size / 1024 > settings.ASSET_SIZE_LIMIT_KB:
        raise WikiException(
            message=f"Limit {settings.ASSET_SIZE_LIMIT_KB} KB the size of the downloaded asset has been exceeded.",
            error_code=WikiErrorCode.ASSET_LIMIT_SIZE_EXCEEDED_EXCEPTION,
            http_status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
        )

    user_repository: UserRepository = UserRepository(session)
    user_db: User = await user_repository.get_user_by_id(user.id)

    workspace_repository: WorkspaceRepository = WorkspaceRepository(session)
    workspace: Workspace = await workspace_repository.get_workspace_by_id(workspace_id)

    asset_repository = AssetRepository(session)
    asset: Asset = await asset_repository.create_asset(asset_type=asset_type,
                                                       name=file.filename,
                                                       size_kb=file.size / 1024,
                                                       uploader_user_id=user_db.id,
                                                       workspace_id=workspace.id)
    ya_storage = YaDiskAssetsStorage(ya_disk)
    link = await ya_storage.upload_asset(asset, file.file)

    return AssetInfoResponse(
        id=asset.id,
        type=asset.type,
        name=asset.name,
        size_kb=asset.size_kb,
        uploader_user=await get_user_info(asset.uploader_user_id, session, is_full=False),
        workspace=await get_workspace_info(asset.workspace_id, session),
        created_at=asset.created_at,
        download_link=link
    )


@asset_storage_router.put(
    "/asset/{asset_id}/",
    response_model=AssetInfoResponse,
    status_code=status.HTTP_200_OK,
    summary="Update Asset info"
)
async def update_asset_info(
        asset_id: UUID,
        update_asset: UpdateAsset,
        is_added_download_link: bool = False,
        session: AsyncSession = Depends(get_db),
        ya_disk: YaDisk = Depends(get_ya_disk_session_storage),
        user: WikiUserHandlerData = Depends(BasePermission(responsibility=ResponsibilityType.VIEWER))
):
    asset_repository = AssetRepository(session)
    asset = await asset_repository.get_asset_by_id(asset_id)
    if update_asset.workspace_id is not None:
        workspace_repository = WorkspaceRepository(session)
        workspace = await workspace_repository.get_workspace_by_id(update_asset.workspace_id)

    updated_asset = await asset_repository.update_asset(asset,
                                                        name=update_asset.name,
                                                        workspace_id=update_asset.workspace_id)
    link = None
    if is_added_download_link:
        ya_storage = YaDiskAssetsStorage(ya_disk)
        link = await ya_storage.download_asset(asset)

    return AssetInfoResponse(
        id=updated_asset.id,
        type=updated_asset.type,
        name=updated_asset.name,
        size_kb=updated_asset.size_kb,
        uploader_user=await get_user_info(updated_asset.uploader_user_id, session, is_full=False),
        workspace=await get_workspace_info(updated_asset.workspace_id, session),
        created_at=updated_asset.created_at,
        download_link=link
    )


@asset_storage_router.delete(
    "/asset/{asset_id}/",
    response_model=BaseResponse,
    status_code=status.HTTP_200_OK,
    summary="Delete Asset"
)
async def delete_asset(
        asset_id: UUID,
        session: AsyncSession = Depends(get_db),
        ya_disk: YaDisk = Depends(get_ya_disk_session_storage),
        user: WikiUserHandlerData = Depends(BasePermission(responsibility=ResponsibilityType.VIEWER))
):
    asset_repository = AssetRepository(session)
    asset = await asset_repository.get_asset_by_id(asset_id)
    await asset_repository.mark_asset_deleted(asset)
    ya_storage = YaDiskAssetsStorage(ya_disk)
    await ya_storage.remove_asset(asset)

    return BaseResponse(msg="The asset has been deleted.")


@asset_storage_router.get(
    "/asset/{asset_id}/",
    response_model=AssetInfoResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Asset info"
)
async def get_asset(
        asset_id: UUID,
        is_added_download_link: bool = False,
        session: AsyncSession = Depends(get_db),
        ya_disk: YaDisk = Depends(get_ya_disk_session_storage),
        user: WikiUserHandlerData = Depends(BasePermission(responsibility=ResponsibilityType.VIEWER))
):
    asset_repository = AssetRepository(session)
    asset = await asset_repository.get_asset_by_id(asset_id)

    link = None
    if is_added_download_link:
        ya_storage = YaDiskAssetsStorage(ya_disk)
        link = await ya_storage.download_asset(asset)

    return AssetInfoResponse(
        id=asset.id,
        type=asset.type,
        name=asset.name,
        size_kb=asset.size_kb,
        uploader_user=await get_user_info(asset.uploader_user_id, session, is_full=False),
        workspace=await get_workspace_info(asset.workspace_id, session),
        created_at=asset.created_at,
        download_link=link
    )


@asset_storage_router.get(
    "/asset/wp/{workspace_id}/",
    response_model=list[AssetInfoResponse],
    status_code=status.HTTP_200_OK,
    summary="Get Assets info for workspace"
)
async def get_assets_for_workspace(
        workspace_id: UUID,
        is_added_download_link: bool = False,
        session: AsyncSession = Depends(get_db),
        ya_disk: YaDisk = Depends(get_ya_disk_session_storage),
        user: WikiUserHandlerData = Depends(BasePermission(responsibility=ResponsibilityType.VIEWER))
):
    workspace_info = await get_workspace_info(workspace_id, session)

    assets_repository = AssetRepository(session)
    assets = await assets_repository.get_assets_for_workspace(workspace_id)

    ya_storage = None
    if is_added_download_link:
        ya_storage = YaDiskAssetsStorage(ya_disk)

    return [AssetInfoResponse(
        id=item.id,
        type=item.type,
        name=item.name,
        size_kb=item.size_kb,
        uploader_user=await get_user_info(item.uploader_user_id, session, is_full=False),
        workspace=workspace_info,
        created_at=item.created_at,
        download_link=await ya_storage.download_asset(item) if ya_storage is not None else None
    ) for item in assets]
