from datetime import datetime
from typing import Optional
from uuid import UUID

from wiki.permissions.domain.enums import DomainPermissionMode
from wiki.models import WikiBase


class CreatePermissionDomain(WikiBase):
    domain: str  # we need to add validation
    mode: DomainPermissionMode


class UpdatePermissionDomain(WikiBase):
    domain: Optional[str] = None
    mode: Optional[DomainPermissionMode] = None


class PermissionDomainIdentifiers(WikiBase):
    id: Optional[UUID] = None
    domain: Optional[str] = None


class PermissionDomainInfoResponse(WikiBase):
    id: UUID
    domain: str
    mode: DomainPermissionMode
    is_enabled: bool
    created_at: datetime
