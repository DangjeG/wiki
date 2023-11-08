from typing import Optional
from uuid import UUID

from sqlalchemy import select, and_
from starlette import status

from wiki.asset.enums import AssetType
from wiki.asset.model import Asset
from wiki.common.exceptions import WikiException, WikiErrorCode
from wiki.database.repository import BaseRepository
from wiki.database.utils import (
    menage_db_not_found_result_method,
    NotFoundResultMode,
    menage_db_commit_method,
    CommitMode
)


class AssetRepository(BaseRepository):
    asset_not_found_exception = WikiException(
        message="Asset not found.",
        error_code=WikiErrorCode.ASSET_NOT_FOUND,
        http_status_code=status.HTTP_404_NOT_FOUND
    )

    @menage_db_commit_method(CommitMode.FLUSH)
    async def create_asset(self,
                           asset_type: AssetType,
                           name: str,
                           size_kb: float,
                           uploader_user_id: UUID,
                           workspace_id: UUID) -> Asset:
        new_asset = Asset(
            type=str(asset_type),
            name=name,
            size_kb=size_kb,
            uploader_user_id=uploader_user_id,
            workspace_id=workspace_id
        )

        self.session.add(new_asset)

        return new_asset

    @menage_db_commit_method(CommitMode.FLUSH)
    async def update_asset(self,
                           asset: Asset,
                           *,
                           name: Optional[str] = None,
                           workspace_id: Optional[UUID] = None):
        if name is not None:
            asset.name = name
        if workspace_id is not None:
            asset.workspace_id = workspace_id

        self.session.add(asset)

        return asset

    @menage_db_not_found_result_method(NotFoundResultMode.EXCEPTION, ex=asset_not_found_exception)
    async def get_asset_by_id(self, asset_id: UUID, is_only_exist: bool = True) -> Asset:
        whereclause = [Asset.id == asset_id]
        if is_only_exist:
            whereclause.append(Asset.is_deleted == False)
        st = select(Asset).where(and_(*whereclause))
        asset_query = (await self.session.execute(st)).scalar()
        return asset_query

    async def get_assets_for_workspace(self, workspace_id: UUID, is_only_exist: bool = True) -> list[Asset]:
        whereclause = [Asset.workspace_id == workspace_id]
        if is_only_exist:
            whereclause.append(Asset.is_deleted == False)
        st = select(Asset).where(and_(*whereclause))
        asset_query = (await self.session.execute(st)).scalars()
        return asset_query

    async def get_all_assets(self, is_only_exist: bool = True) -> list[Asset]:
        whereclause = []
        if is_only_exist:
            whereclause.append(Asset.is_deleted == False)
        st = select(Asset).where(and_(*whereclause))
        asset_query = (await self.session.execute(st)).scalars()
        return asset_query

    @menage_db_commit_method(CommitMode.FLUSH)
    async def mark_asset_deleted(self, asset: Asset):
        asset.is_deleted = True

        self.session.add(asset)
