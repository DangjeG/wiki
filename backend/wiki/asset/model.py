from uuid import UUID

from sqlalchemy import Column, Uuid, String, ForeignKey, Float
from uuid_extensions import uuid7

from wiki.common.models import DeletedMixin
from wiki.database.core import Base


class Asset(Base, DeletedMixin):
    id = Column(Uuid, default=uuid7, primary_key=True, nullable=False)
    type = Column(String, nullable=False)  # AssetType

    name = Column(String, nullable=False)
    size_kb = Column(Float, nullable=False)  # Asset size in kilobytes

    uploader_user_id = Column(ForeignKey("user.id"), nullable=False)
    workspace_id = Column(ForeignKey("workspace.id"), nullable=False)

