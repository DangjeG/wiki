from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from wiki.auth.enums import AuthorizationMode
from wiki.common.schemas import ExternalUserHandlerData
from wiki.database.deps import get_db
from wiki.organization.repository import OrganizationRepository
from wiki.permissions.base import BasePermission
from wiki.wiki_api_client.enums import ResponsibilityType
from wiki.common.exceptions import WikiException, WikiErrorCode
from wiki.common.schemas import WikiUserHandlerData
from wiki.organization.schemas import (
    OrganizationIdentifiers,
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
        user: ExternalUserHandlerData | WikiUserHandlerData =
        Depends(BasePermission(authorisation_mode=AuthorizationMode.UNAUTHORIZED)),
        organization_get: OrganizationIdentifiers = Depends(),
        session: AsyncSession = Depends(get_db)
):
    organization_repo: OrganizationRepository = OrganizationRepository(session)
    org = await organization_repo.get_organization_by_id(organization_get.id)

    return OrganizationInfoResponse(
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
        user: WikiUserHandlerData = Depends(BasePermission(responsibility=ResponsibilityType.ADMIN)),
        session: AsyncSession = Depends(get_db),
        organization_identifiers: OrganizationIdentifiers = Depends(),
        update_org: UpdateOrganization = Depends()):
    organization_repository: OrganizationRepository = OrganizationRepository(session)

    if organization_identifiers.id is not None:
        organization = await organization_repository.get_organization_by_id(organization_identifiers.id)
    else:
        raise WikiException(
            message="Organization not found.",
            error_code=WikiErrorCode.ORGANIZATION_NOT_FOUND,
            http_status_code=status.HTTP_404_NOT_FOUND
        )

    updated_organization = await organization_repository.update_organization(
        organization_id=organization.id,
        name=update_org.name,
        description=update_org.description,
        access=update_org.access
    )

    return OrganizationInfoResponse(
        name=updated_organization.name,
        description=updated_organization.description,
        access=updated_organization.access
    )
