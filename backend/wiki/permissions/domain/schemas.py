from wiki.permissions.domain.enums import DomainPermissionMode
from wiki.models import WikiBase


class CreatePermissionDomain(WikiBase):
    domain: str  # we need to add validation
    status: DomainPermissionMode
