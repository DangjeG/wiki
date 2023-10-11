from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import Column, Uuid, String, DateTime, ForeignKey, SmallInteger
from uuid_extensions import uuid7

from wiki.common.models import EnabledDeletedMixin
from wiki.database.core import Base
from wiki.wiki_api_client.enums import ResponsibilityType


class WikiApiClient(Base, EnabledDeletedMixin):
    id = Column(Uuid, default=uuid7, primary_key=True, nullable=False)
    description = Column(String(256), nullable=True)
    responsibility = Column(SmallInteger, nullable=False, default=ResponsibilityType.VIEWER)

    def __init__(self,
                 description: Optional[str] = None,
                 responsibility: ResponsibilityType = ResponsibilityType.VIEWER,
                 is_enabled: bool = True):
        self.description = description
        self.responsibility = responsibility
        self.is_enabled = is_enabled


class WikiApiKey(Base, EnabledDeletedMixin):
    id = Column(Uuid, default=uuid7, primary_key=True, nullable=False)
    api_key_hash = Column(String(512), nullable=False, index=True, unique=True)
    api_key_prefix = Column(String(8), nullable=False)
    expires_date = Column(DateTime(timezone=True), nullable=False)

    owner_id = Column(ForeignKey("wiki_api_client.id"), nullable=False)

    def __init__(self,
                 api_key_hash: str,
                 api_key_prefix: str,
                 expires_date: datetime,
                 owner_id: UUID):
        self.api_key_hash = api_key_hash
        self.api_key_prefix = api_key_prefix
        self.expires_date = expires_date
        self.owner_id = owner_id
