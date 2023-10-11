from abc import ABC
from typing import Optional

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from wiki.common.exceptions import WikiException, WikiErrorCode
from wiki.database.deps import get_db
from wiki.organization.models import Organization
from wiki.organization.repository import OrganizationRepository
from wiki.permissions.domain.deps import DomainPermission
from wiki.user.repository import UserRepository
from wiki.user.schemas import CreateUser


class SignUpPermission(ABC):
    domain_permission: DomainPermission

    def __init__(self, domain_permission: Optional[DomainPermission] = None):
        self.domain_permission = domain_permission or DomainPermission()

    async def __call__(self, create_user: CreateUser, session: AsyncSession = Depends(get_db)):
        await self.domain_permission(create_user.email.split("@")[1])
        if not create_user.is_user_agreement_accepted:
            raise WikiException(
                message="You must accept the user agreement.",
                error_code=WikiErrorCode.USER_NOT_SPECIFIED,
                http_status_code=status.HTTP_400_BAD_REQUEST
            )
        user_repository: UserRepository = UserRepository(session)
        is_available: bool = await user_repository.check_user_identification_data_is_available(create_user.email,
                                                                                               create_user.username)
        if not is_available:
            raise WikiException(
                message="Your username or email is not available or you have already sent an application.",
                error_code=WikiErrorCode.USER_NOT_SPECIFIED,
                http_status_code=status.HTTP_409_CONFLICT
            )
        organisation_repository: OrganizationRepository(session)
        organization: Organization = await organisation_repository.get_organization_by_id(create_user.organization_id)
