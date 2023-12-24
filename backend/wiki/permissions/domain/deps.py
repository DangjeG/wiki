from abc import ABC

from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from wiki.common.exceptions import WikiException, WikiErrorCode
from wiki.permissions.domain.enums import DomainPermissionMode
from wiki.permissions.domain.repository import PermissionDomainRepository


class DomainPermission(ABC):
    permission_mode: DomainPermissionMode

    def __init__(self, permission_mode: DomainPermissionMode = DomainPermissionMode.ACCEPT):
        self.permission_mode = permission_mode

    async def __call__(self, domain: str, session: AsyncSession):
        permission_domain_repo: PermissionDomainRepository = PermissionDomainRepository(session)
        permission_mode: DomainPermissionMode = await permission_domain_repo.get_domain_permission_mode(domain)
        if self.permission_mode > permission_mode:
            raise WikiException(
                message=f"The domain {domain} doesn't have permission.",
                error_code=WikiErrorCode.PERMISSION_DOMAIN_ERROR,
                http_status_code=status.HTTP_403_FORBIDDEN
            )
