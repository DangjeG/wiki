from enum import Enum
from uuid import UUID

from sqlalchemy import Column, Uuid, ForeignKey, String
from uuid_extensions import uuid7

from wiki.common.models import EnabledDeletedMixin
from wiki.database.core import Base


class TypeBlock(Enum):
    IMG = "IMG"
    TEXT = "TEXT"
    FILE = "FILE"
    VIDEO = "VIDEO"


class Block(Base, EnabledDeletedMixin):
    id = Column(Uuid, default=uuid7, primary_key=True, nullable=False)

    type_block = Column(String, nullable=False, default=TypeBlock.TEXT)

    workspace_id = Column(ForeignKey("workspace.id"), unique=True, nullable=False)
    document_id = Column(ForeignKey("document.id"), unique=True, nullable=False)

    def __init__(self,
                 document_id: UUID,
                 workspace_id: UUID,
                 type_block: TypeBlock):
        self.document_id = document_id
        self.workspace_id = workspace_id
        self.type_block = type_block
