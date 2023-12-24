from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import HttpUrl

from wiki.asset.enums import AssetType
from wiki.models import WikiBase
from wiki.user.schemas import UserBaseInfoResponse
from wiki.wiki_workspace.schemas import WorkspaceInfoResponse


class AssetInfoResponse(WikiBase):
    id: UUID
    type: AssetType
    name: str
    size_kb: float
    uploader_user: UserBaseInfoResponse
    workspace: WorkspaceInfoResponse
    created_at: datetime
    download_link: Optional[HttpUrl] = None


class UpdateAsset(WikiBase):
    name: Optional[str] = None
    workspace_id: Optional[UUID] = None
