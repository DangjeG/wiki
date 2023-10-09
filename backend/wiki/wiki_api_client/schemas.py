from datetime import datetime
from typing import Optional

from sqlalchemy import UUID

from wiki.models import WikiBase
from wiki.wiki_api_client.enums import ResponsibilityType


class CreateWikiApiClient(WikiBase):
    description: Optional[str] = None
    responsibility: ResponsibilityType = ResponsibilityType.VIEWER
    is_enabled: bool = True


class CreateWikiApiKey(WikiBase):
    api_key_hash: str
    api_key_prefix: str
    expires_date: datetime
    owner_id: UUID
