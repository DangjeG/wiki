from typing import Optional
from uuid import UUID

from wiki.models import WikiBase
from wiki.organization.enums import OrganizationAccessType


class CreateOrganization(WikiBase):
    name: str
    description: Optional[str] = None
    access: OrganizationAccessType


class OrganizationInfoResponse(WikiBase):
    id: UUID
    name: str
    description: Optional[str]
    access: OrganizationAccessType


class UpdateOrganization(WikiBase):
    name: Optional[str] = None
    description: Optional[str] = None
    access: Optional[OrganizationAccessType] = None


class OrganizationFilter(WikiBase):
    name: Optional[str] = None
    description: Optional[str] = None
    access: Optional[OrganizationAccessType] = None
