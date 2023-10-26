from uuid import UUID

from sqlalchemy import select, bindparam, and_
from starlette import status

from wiki.common.exceptions import WikiException, WikiErrorCode
from wiki.database.repository import BaseRepository
from wiki.database.utils import (
    menage_db_not_found_result_method,
    NotFoundResultMode,
    CommitMode,
    menage_db_commit_method
)
from wiki.organization.models import Organization
from wiki.organization.schemas import CreateOrganization, OrganizationFilter


class OrganizationRepository(BaseRepository):
    _organization_not_found_exception = WikiException(
        message="Organization not found.",
        error_code=WikiErrorCode.ORGANIZATION_NOT_FOUND,
        http_status_code=status.HTTP_404_NOT_FOUND
    )

    @menage_db_not_found_result_method(NotFoundResultMode.EXCEPTION, ex=_organization_not_found_exception)
    async def get_organization_by_id(self, organization_id: UUID) -> Organization:
        organization_query = await self.session.get(Organization, organization_id)
        return organization_query

    async def get_all_organization_filter(self, organization_filter: OrganizationFilter) -> list[Organization]:
        filters = []
        if organization_filter.name is not None:
            filters.append(Organization.name.ilike(f'%{organization_filter.name}%'))
        if organization_filter.access is not None:
            filters.append(Organization.access.like(str(organization_filter.access)))
        if organization_filter.description is not None:
            filters.append(Organization.description.ilike(f'%{organization_filter.description}%'))

        result = await self.session.execute(select(Organization).where(and_(*filters)))

        return result.scalars().all()

    async def get_all_organization(self) -> list[Organization]:
        organization_query = await self.session.execute(select(Organization))
        result = organization_query.scalars().all()
        return result

    @menage_db_commit_method(CommitMode.FLUSH)
    async def create_organization(self, create_organization: CreateOrganization) -> Organization:
        new_organization = Organization(
            name=create_organization.name,
            description=create_organization.description,
            access=str(create_organization.access)
        )
        self.session.add(new_organization)
        return new_organization

    @menage_db_commit_method(CommitMode.FLUSH)
    async def update_organization(self,
                                  organization_id: UUID,
                                  *,
                                  name: str,
                                  description: str,
                                  access: str) -> Organization:
        organization: Organization = await self.get_organization_by_id(organization_id)

        if name is not None:
            organization.name = name
        if description is not None:
            organization.description = description
        if access is not None:
            organization.access = access

        self.session.add(organization)

        return organization
