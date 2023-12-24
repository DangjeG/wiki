from typing import Optional
from uuid import UUID

from sqlalchemy import select, and_
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
from wiki.permissions.domain.schemas import CreatePermissionDomain, PermissionDomainFilter


class PermissionDomainRepository(BaseRepository):
    permission_domain_not_found_exception = WikiException(
        message="Permission domain not found.",
        error_code=WikiErrorCode.PERMISSION_DOMAIN_NOT_FOUND,
        http_status_code=status.HTTP_404_NOT_FOUND
    )

    @menage_db_not_found_result_method(NotFoundResultMode.EXCEPTION, ex=permission_domain_not_found_exception)
    async def get_permission_domain_by_id(self, user_id: UUID) -> PermissionDomain:
        domain_query = await self.session.get(PermissionDomain, user_id)
        return domain_query

    @menage_db_not_found_result_method(NotFoundResultMode.NONE)
    async def get_permission_domain_by_domain_name(self, domain: str) -> Optional[PermissionDomain]:
        st = select(PermissionDomain).where(PermissionDomain.domain == domain.lower())
        domain_query = (await self.session.execute(st)).scalar()
        return domain_query

    async def get_all_permission_domains_filter(self, permission_domain_filter: PermissionDomainFilter) -> list[PermissionDomain]:
        filters = []
        if permission_domain_filter.domain is not None:
            filters.append(select(PermissionDomain.domain.ilike(f'%{permission_domain_filter.domain}%')))
        if permission_domain_filter.mode is not None:
            filters.append(select(PermissionDomain.mode.like(str(permission_domain_filter.mode))))
        if permission_domain_filter.is_enabled is not None:
            filters.append(select(PermissionDomain.is_enabled.like(permission_domain_filter.is_enabled)))

        result = await self.session.execute(select(PermissionDomain).where(and_(*filters)))

        return result.scalars().all()

    async def get_all_permission_domains(self) -> list[PermissionDomain]:
        users_query = await self.session.execute(select(PermissionDomain))
        res = users_query.scalars().all()
        return res

    async def get_domain_permission_mode(self, domain: str) -> DomainPermissionMode:
        st = select(PermissionDomain).where(PermissionDomain.domain == domain.lower())
        domain_query: PermissionDomain = (await self.session.execute(st)).scalar()
        if domain_query is not None:
            return DomainPermissionMode(domain_query.mode)
        else:
            return DomainPermissionMode.REFUSE

    @menage_db_commit_method(CommitMode.FLUSH)
    async def create_permission_domain(self, create_domain: CreatePermissionDomain):
        new_domain = PermissionDomain(
            domain=create_domain.domain.lower(),
            mode=str(create_domain.mode)
        )

        self.session.add(new_domain)

        return new_domain

    @menage_db_commit_method(CommitMode.FLUSH)
    async def update_permission_domain(self,
                                       domain_id: UUID,
                                       *,
                                       domain: Optional[str] = None,
                                       domain_mode: Optional[DomainPermissionMode] = None) -> PermissionDomain:
        permission_domain: PermissionDomain = await self.get_permission_domain_by_id(domain_id)
        if domain is not None:
            permission_domain.domain = domain.lower()
        if domain_mode is not None:
            permission_domain.mode = str(domain_mode)

        self.session.add(permission_domain)

        return permission_domain
