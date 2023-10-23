from enum import Enum
from uuid import UUID

from sqlalchemy import Column, Uuid, String, ForeignKey
from uuid_extensions import uuid7

from wiki.common.models import EnabledDeletedMixin
from wiki.database.core import Base

class Workspace(Base, EnabledDeletedMixin):
    id = Column(Uuid, default=uuid7, primary_key=True, nullable=False)

    title = Column(String, nullable=False)

    owner_wiki_api_client = Column(ForeignKey("wiki_api_client.id"), unique=True, nullable=False)

    def __init__(self,
                 title: str,
                 owner_wiki_api_client: UUID):
        self.title = title
        self.owner_wiki_api_client = owner_wiki_api_client
