from typing import Optional
from uuid import UUID

from sqlalchemy import select
from starlette import status

from wiki.permissions.domain.enums import DomainPermissionMode
from wiki.common.exceptions import WikiException, WikiErrorCode
from wiki.database.repository import BaseRepository
from wiki.database.utils import (
    menage_db_commit_method,
    CommitMode,
    menage_db_not_found_result_method,
    NotFoundResultMode
)
from wiki.permissions.domain.models import PermissionDomain
from wiki.permissions.domain.schemas import CreatePermissionDomain


class PermissionDomainRepository(BaseRepository):
    _permission_domain_not_found_exception = WikiException(
        message="Permission domain not found.",
        error_code=WikiErrorCode.PERMISSION_DOMAIN_NOT_FOUND,
        http_status_code=status.HTTP_404_NOT_FOUND
    )

    @menage_db_not_found_result_method(NotFoundResultMode.EXCEPTION, ex=_permission_domain_not_found_exception)
    async def get_permission_domain_by_id(self, user_id: UUID) -> PermissionDomain:
        domain_query = await self.session.get(PermissionDomain, user_id)
        return domain_query

    async def get_all_permission_domains(self) -> list[PermissionDomain]:
        users_query = await self.session.execute(select(PermissionDomain))
        res = users_query.scalars().all()
        return res

    async def get_domain_permission_mode(self, domain: str) -> DomainPermissionMode:
        st = select(PermissionDomain).where(PermissionDomain.domain == domain)
        domain_query: PermissionDomain = (await self.session.execute(st)).scalar()
        if domain_query is not None:
            return DomainPermissionMode(domain_query.mode)
        else:
            return DomainPermissionMode.REFUSE

    @menage_db_commit_method(CommitMode.FLUSH)
    async def create_permission_domain(self, create_domain: CreatePermissionDomain):
        new_domain = PermissionDomain(
            domain=create_domain.domain,
            mode=str(create_domain.mode)
        )

        self.session.add(new_domain)

        return new_domain

    @menage_db_commit_method(CommitMode.FLUSH)
    async def update_permission_domain(self,
                                       domain_id: UUID,
                                       *,
                                       domain: Optional[str] = None,
                                       domain_status: Optional[DomainPermissionMode] = None) -> PermissionDomain:
        permission_domain: PermissionDomain = await self.get_permission_domain_by_id(domain_id)
        if domain is not None:
            permission_domain.domain = domain
        if domain_status is not None:
            permission_domain.mode = str(domain_status)

        self.session.add(permission_domain)

        return permission_domain
