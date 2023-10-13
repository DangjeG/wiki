from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from wiki.auth.enums import AuthorizationMode
from wiki.common.schemas import ExternalUserHandlerData
from wiki.database.deps import get_db
from wiki.organization.models import Organization
from wiki.organization.repository import OrganizationRepository
from wiki.permissions.base import BasePermission
from wiki.wiki_api_client.enums import ResponsibilityType
from wiki.common.schemas import WikiUserHandlerData
from wiki.organization.schemas import (
    OrganizationInfoResponse,
    CreateOrganization,
    UpdateOrganization,
)


organization_router = APIRouter()


@organization_router.get(
    "/info",
    response_model=OrganizationInfoResponse,
    status_code=status.HTTP_200_OK,
    description="Get organization by id."
)
async def get_organization(
        organization_id: UUID,
        user: ExternalUserHandlerData | WikiUserHandlerData =
        Depends(BasePermission(authorisation_mode=AuthorizationMode.UNAUTHORIZED)),
        session: AsyncSession = Depends(get_db)
):
    organization_repo: OrganizationRepository = OrganizationRepository(session)
    org: Organization = await organization_repo.get_organization_by_id(organization_id)

    return OrganizationInfoResponse(
        id=org.id,
        name=org.name,
        description=org.description,
        access=org.access
    )


@organization_router.post(
    "/",
    response_model=OrganizationInfoResponse,
    status_code=status.HTTP_202_ACCEPTED,
    description="Create organization."
)
async def create_organization(user: WikiUserHandlerData = Depends(BasePermission(responsibility=ResponsibilityType.ADMIN)),
                              organization: CreateOrganization = Depends(),
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
        id=organization.id,
        name=organization.name,
        description=organization.description,
        access=organization.access
    )


@organization_router.get(
    "/all",
    response_model=list[OrganizationInfoResponse],
    status_code=status.HTTP_200_OK,
    description="Get all organizations.",
)
async def get_organizations(
        user: ExternalUserHandlerData | WikiUserHandlerData =
        Depends(BasePermission(authorisation_mode=AuthorizationMode.UNAUTHORIZED)),
        session: AsyncSession = Depends(get_db)
):
    organization_repository: OrganizationRepository = OrganizationRepository(session)

    organizations: list[OrganizationInfoResponse] = await organization_repository.get_all_organization()

    result_organization: list[OrganizationInfoResponse] = []

    for organization in organizations:
        result_organization.append(
            OrganizationInfoResponse(
                id=organization.id,
                name=organization.name,
                description=organization.description,
                access=organization.access
            )
        )

    return result_organization


@organization_router.put(
    "/",
    response_model=OrganizationInfoResponse,
    status_code=status.HTTP_200_OK,
    description="Update organization."
)
async def update_organizations(
        organization_id: UUID,
        update_org: UpdateOrganization,
        user: WikiUserHandlerData = Depends(BasePermission(responsibility=ResponsibilityType.ADMIN)),
        session: AsyncSession = Depends(get_db)):
    organization_repository: OrganizationRepository = OrganizationRepository(session)

    updated_organization: Organization = await organization_repository.update_organization(
        organization_id=organization_id,
        name=update_org.name,
        description=update_org.description,
        access=update_org.access
    )

    return OrganizationInfoResponse(
        id=updated_organization.id,
        name=updated_organization.name,
        description=updated_organization.description,
        access=updated_organization.access
    )
