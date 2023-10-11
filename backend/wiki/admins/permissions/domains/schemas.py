from wiki.admins.permissions.domains.enums import DomainPermissionStatus
from wiki.models import WikiBase


class CreatePermissionDomain(WikiBase):
    domain: str  # we need to add validation
    status: DomainPermissionStatus
