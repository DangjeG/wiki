from sqlalchemy import Column, Uuid, String, DateTime
from uuid_extensions import uuid7

from wiki.admins.permissions.domains.enums import DomainPermissionStatus
from wiki.database.core import Base
from wiki.database.utils import utcnow


class PermissionDomain(Base):
    id = Column(Uuid, default=uuid7, primary_key=True, nullable=False)
    domain = Column(String, unique=True, nullable=False)
    created_date = Column(DateTime(timezone=True), nullable=False, default=utcnow())
    status = Column(String, nullable=False, default=DomainPermissionStatus.ACCEPT_APPLICATION)

    def __init__(self,
                 domain: str,
                 status: DomainPermissionStatus):
        self.domain = domain
        self.status = status

