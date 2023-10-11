from sqlalchemy import Column, Uuid, String, SmallInteger
from uuid_extensions import uuid7

from wiki.permissions.domain.enums import DomainPermissionMode
from wiki.common.models import EnabledDeletedMixin
from wiki.database.core import Base


class PermissionDomain(Base, EnabledDeletedMixin):
    id = Column(Uuid, default=uuid7, primary_key=True, nullable=False)
    domain = Column(String, unique=True, nullable=False)
    mode = Column(SmallInteger, nullable=False, default=DomainPermissionMode.ACCEPT)

    def __init__(self,
                 domain: str,
                 mode: DomainPermissionMode):
        self.domain = domain
        self.mode = mode
