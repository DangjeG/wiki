from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from wiki.admins.permissions.domains.enums import DomainPermissionStatus
from wiki.admins.permissions.domains.repository import PermissionDomainRepository
from wiki.auth.resolvers.base import Resolver
from wiki.common.exceptions import WikiException, WikiErrorCode


class EmailResolver(Resolver):
    permission_domain_repo: PermissionDomainRepository

    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.permission_domain_repo = PermissionDomainRepository(session)

    async def resolve(self, candidate: EmailStr):
        email_domain = candidate.split("@")[1]
        permission_status: DomainPermissionStatus = await self.permission_domain_repo.get_domain_permission_status(email_domain)
        match permission_status:
            case DomainPermissionStatus.ACCEPT_APPLICATION:
                return False
            case DomainPermissionStatus.ACCEPT_WITHOUT_CONSIDERATION:
                return True
            case DomainPermissionStatus.REFUSE:
                raise WikiException(
                    message="Registration requests with your email will not be accepted.",
                    error_code=WikiErrorCode.EMAIL_NOT_ALLOWED,
                    http_status_code=status.HTTP_400_BAD_REQUEST
                )
