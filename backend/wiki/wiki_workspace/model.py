from uuid import UUID

from sqlalchemy import Column, Uuid, String, ForeignKey
from uuid_extensions import uuid7

from wiki.common.models import EnabledDeletedMixin
from wiki.database.core import Base


class Workspace(Base, EnabledDeletedMixin):
    id = Column(Uuid, default=uuid7, primary_key=True, nullable=False)

    title = Column(String, nullable=False)

    owner_user_id = Column(ForeignKey("user.id"), nullable=False)

    def __init__(self,
                 title: str,
                 owner_user_id: UUID):
        self.title = title
        self.owner_user_id = owner_user_id
