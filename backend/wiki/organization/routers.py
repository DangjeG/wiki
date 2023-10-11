from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from wiki.common.exceptions import WikiException, WikiErrorCode
from wiki.database.deps import get_db
from wiki.organization.models import Organization
from wiki.organization.repository import OrganizationRepository
from wiki.organization.schemas import OrganizationIdentifiers, OrganizationInfoResponse, CreateOrganization, \
    UpdateOrganization

organization_router = APIRouter()

@organization_router.get(
    "/info",
    response_model=OrganizationInfoResponse,
    status_code=status.HTTP_200_OK,
    description="Get organization by id."
)
async def get_organization(organization_get: OrganizationIdentifiers = Depends(),
                           session: AsyncSession = Depends(get_db)):

    organization_repository: OrganizationRepository = OrganizationRepository(session)

    organization: Optional[Organization] = None

    if organization_get.id is not None:
        organization = await organization_repository.get_organization_by_id(organization_get.id)
    else:
        raise WikiException(
            message="Organization not found.",
            error_code=WikiErrorCode.ORGANIZATION_NOT_FOUND,
            http_status_code=status.HTTP_404_NOT_FOUND
        )

    return OrganizationInfoResponse(
        name=organization.name,
        description=organization.description,
        access=organization.access
    )


@organization_router.post(
    "/",
    response_model=OrganizationInfoResponse,
    status_code=status.HTTP_200_OK,
    description="Create organization."
)
async def create_organization(organization: CreateOrganization = Depends(),
                              session: AsyncSession = Depends(get_db)):
    organization_repository: OrganizationRepository = OrganizationRepository(session)

    organization = await organization_repository.create_organization(
        CreateOrganization(
            id=organization.id,
            name=organization.name,
            description=organization.description,
            access=organization.access
        )
    )

    return OrganizationInfoResponse(
        name=organization.name,
        description=organization.description,
        access=organization.access
    )

@organization_router.get(
    "/",
    response_model=list[OrganizationInfoResponse],
    status_code=status.HTTP_200_OK,
    description="Get all organization."
)
async def get_organizations(session: AsyncSession = Depends(get_db)):
    organization_repository: OrganizationRepository = OrganizationRepository(session)

    organizations: list[OrganizationInfoResponse] = await organization_repository.get_all_organization()

    result_organization: list[OrganizationInfoResponse] = []

    for organization in organizations:
        result_organization.append(
            OrganizationInfoResponse(
                name=organization.name,
                description=organization.description,
                access=organization.access
            )
        )

    return result_organization

@organization_router.post(
    "/",
    response_model=OrganizationInfoResponse,
    status_code=status.HTTP_200_OK,
    description="Update organization."
)
async def update_organizations(session: AsyncSession = Depends(get_db),
                               organization_identifiers: OrganizationIdentifiers = Depends(),
                               update_organization: UpdateOrganization = Depends()):
    organization_repository: OrganizationRepository = OrganizationRepository(session)

    organization: Optional[Organization] = None

    if organization_identifiers.id is not None:
        organization = await organization_repository.get_organization_by_id(organization_identifiers.id)
    else:
        raise WikiException(
            message="Organization not found.",
            error_code=WikiErrorCode.ORGANIZATION_NOT_FOUND,
            http_status_code=status.HTTP_404_NOT_FOUND
        )

    await organization_repository.update_organization(
        organization_id=organization.id,
        name=update_organization.name,
        description=update_organizations.description,
        access=update_organization.access
    )

    return OrganizationInfoResponse(
        name=update_organization.name,
        description=update_organizations.description,
        access=update_organization.access
    )

