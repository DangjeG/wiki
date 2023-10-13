from sqlalchemy import Column, Uuid, String
from uuid_extensions import uuid7

from wiki.common.models import TimeStampMixin
from wiki.database.core import Base
from wiki.organization.enums import OrganizationAccessType


class Organization(Base, TimeStampMixin):
    id = Column(Uuid, default=uuid7, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String(256), nullable=True)
    access = Column(String, nullable=False, default=str(OrganizationAccessType.WEB_ONLY))
