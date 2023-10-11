from typing import Optional
from uuid import UUID

from wiki.models import WikiBase
from wiki.organization.enums import OrganizationAccessType


class CreateOrganization(WikiBase):
    name: str
    description: str
    access: OrganizationAccessType


class OrganizationIdentifiers(WikiBase):
    id: Optional[UUID] = None

class OrganizationInfoResponse(WikiBase):
    name: str
    description: str
    access: OrganizationAccessType
