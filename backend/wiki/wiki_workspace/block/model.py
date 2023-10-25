from enum import Enum
from uuid import UUID

from sqlalchemy import Column, Uuid, ForeignKey, String
from uuid_extensions import uuid7

from wiki.common.enums import WikiBaseEnum
from wiki.common.models import EnabledDeletedMixin
from wiki.database.core import Base


class TypeBlock(WikiBaseEnum):
    IMG = "IMG"
    TEXT = "TEXT"
    FILE = "FILE"
    VIDEO = "VIDEO"


class Block(Base, EnabledDeletedMixin):
    id = Column(Uuid, default=uuid7, primary_key=True, nullable=False)

    type_block = Column(String, nullable=False, default=str(TypeBlock.TEXT))

    document_id = Column(ForeignKey("document.id"), nullable=False)

    def __init__(self,
                 document_id: UUID,
                 type_block: TypeBlock):
        self.document_id = document_id
        self.type_block = str(type_block)
