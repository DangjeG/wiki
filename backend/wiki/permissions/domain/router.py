from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from wiki.common.exceptions import WikiException, WikiErrorCode
from wiki.common.schemas import WikiUserHandlerData
from wiki.database.deps import get_db
from wiki.permissions.base import BasePermission
from wiki.permissions.domain.models import PermissionDomain
from wiki.permissions.domain.repository import PermissionDomainRepository
from wiki.permissions.domain.schemas import (
    CreatePermissionDomain,
    PermissionDomainInfoResponse,
    PermissionDomainIdentifiers,
    UpdatePermissionDomain
)
from wiki.wiki_api_client.enums import ResponsibilityType

permission_domain_router = APIRouter()


@permission_domain_router.post(
    "/",
    response_model=PermissionDomainInfoResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Create a new domain permission for signup"
)
async def create_permission_domain(
        create_domain: CreatePermissionDomain,
        user: WikiUserHandlerData = Depends(BasePermission(responsibility=ResponsibilityType.ADMIN)),
        session: AsyncSession = Depends(get_db)):
    domain_repository: PermissionDomainRepository = PermissionDomainRepository(session)
    permission_domain = await domain_repository.get_permission_domain_by_domain_name(create_domain.domain)
    if permission_domain is not None:
        raise WikiException(
            message="Domain permission already exists",
            error_code=WikiErrorCode.PERMISSION_DOMAIN_NOT_SPECIFIED,
            http_status_code=status.HTTP_400_BAD_REQUEST
        )
    new_permission_domain: PermissionDomain = await domain_repository.create_permission_domain(create_domain)

    return PermissionDomainInfoResponse(
        id=new_permission_domain.id,
        domain=new_permission_domain.domain,
        mode=new_permission_domain.mode,
        is_enabled=new_permission_domain.is_enabled,
        created_at=new_permission_domain.created_at
    )


@permission_domain_router.get(
    "/info",
    response_model=PermissionDomainInfoResponse,
    status_code=status.HTTP_200_OK,
    summary="Get permission domain by id or domain name"
)
async def get_permission_domain_info(
        identifier: PermissionDomainIdentifiers = Depends(),
        user: WikiUserHandlerData = Depends(BasePermission(responsibility=ResponsibilityType.ADMIN)),
        session: AsyncSession = Depends(get_db)
):
    domain_db = await _get_permission_domain(session, identifier)

    return PermissionDomainInfoResponse(
        id=domain_db.id,
        domain=domain_db.domain,
        mode=domain_db.mode,
        is_enabled=domain_db.is_enabled,
        created_at=domain_db.created_at
    )


async def _get_permission_domain(session: AsyncSession, identifier: PermissionDomainIdentifiers):
    domain_repository: PermissionDomainRepository = PermissionDomainRepository(session)
    if identifier.id is not None:
        domain_db: PermissionDomain = await domain_repository.get_permission_domain_by_id(identifier.id)
    elif identifier.domain is not None:
        domain_db: PermissionDomain = await domain_repository.get_permission_domain_by_domain_name(identifier.domain)
        if domain_db is None:
            raise domain_repository.permission_domain_not_found_exception
    else:
        raise domain_repository.permission_domain_not_found_exception

    return domain_db


@permission_domain_router.get(
    "/all",
    response_model=list[PermissionDomainInfoResponse],
    status_code=status.HTTP_200_OK,
    summary="Get all permission domain"
)
async def get_permission_domains(
        user: WikiUserHandlerData = Depends(BasePermission(responsibility=ResponsibilityType.ADMIN)),
        session: AsyncSession = Depends(get_db)
):
    domain_repository: PermissionDomainRepository = PermissionDomainRepository(session)
    domains: list[PermissionDomain] = await domain_repository.get_all_permission_domains()
    result_domains: list[PermissionDomainInfoResponse] = []

    for domain in domains:
        result_domains.append(PermissionDomainInfoResponse(
            id=domain.id,
            domain=domain.domain,
            mode=domain.mode,
            is_enabled=domain.is_enabled,
            created_at=domain.created_at
        ))

    return result_domains


@permission_domain_router.put(
    "/",
    response_model=PermissionDomainInfoResponse,
    status_code=status.HTTP_200_OK,
    summary="Update permission domain by id or domain name"
)
async def update_permission_domain(
        domain_update: UpdatePermissionDomain,
        identifier: PermissionDomainIdentifiers = Depends(),
        user: WikiUserHandlerData = Depends(BasePermission(responsibility=ResponsibilityType.ADMIN)),
        session: AsyncSession = Depends(get_db)
):
    domain_db = await _get_permission_domain(session, identifier)
    domain_repository: PermissionDomainRepository = PermissionDomainRepository(session)
    updated_domain: PermissionDomain = await domain_repository.update_permission_domain(domain_db.id,
                                                                                        domain=domain_update.domain,
                                                                                        domain_mode=domain_update.mode)

    return PermissionDomainInfoResponse(
        id=updated_domain.id,
        domain=updated_domain.domain,
        mode=updated_domain.mode,
        is_enabled=updated_domain.is_enabled,
        created_at=updated_domain.created_at
    )
