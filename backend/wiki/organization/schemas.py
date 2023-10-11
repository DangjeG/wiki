from typing import Optional
from uuid import UUID

from wiki.models import WikiBase
from wiki.organization.enums import OrganizationAccessType


class CreateOrganization(WikiBase):
    name: str
    description: str
    access: OrganizationAccessType


class OrganizationIdentifiers(WikiBase):
    id: UUID


class OrganizationInfoResponse(WikiBase):
    name: str
    description: str
    access: OrganizationAccessType


class UpdateOrganization(WikiBase):
    name: Optional[str] = None
    description: Optional[str] = None
    access: Optional[OrganizationAccessType] = None
