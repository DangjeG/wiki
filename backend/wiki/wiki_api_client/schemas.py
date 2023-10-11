from datetime import datetime
from typing import Optional
from uuid import UUID

from wiki.models import WikiBase
from wiki.wiki_api_client.enums import ResponsibilityType


class CreateWikiApiClient(WikiBase):
    description: Optional[str] = None
    responsibility: ResponsibilityType = ResponsibilityType.VIEWER
    is_enabled: bool = True


class WikiApiClientInfoResponse(WikiBase):
    description: Optional[str] = None
    responsibility: ResponsibilityType = ResponsibilityType.VIEWER
    is_enabled: bool = True


class UpdateWikiApiClient(WikiBase):
    description: Optional[str] = None
    responsibility: Optional[ResponsibilityType] = None
    is_enabled: Optional[bool] = None


class CreateWikiApiKey(WikiBase):
    api_key_hash: str
    api_key_prefix: str
    expires_date: datetime
    owner_id: UUID


class WikiApiKeyInfoResponse(WikiBase):
    api_key: str
    expires_date: datetime
    create_date: datetime
    api_key_prefix: str

