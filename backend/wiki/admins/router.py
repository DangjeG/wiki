from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from wiki.common.exceptions import WikiException, WikiErrorCode
from wiki.common.schemas import WikiUserHandlerData
from wiki.database.deps import get_db
from wiki.organization.models import Organization
from wiki.organization.repository import OrganizationRepository
from wiki.organization.schemas import OrganizationInfoResponse
from wiki.permissions.base import BasePermission
from wiki.user.models import User
from wiki.user.repository import UserRepository
from wiki.user.schemas import UserInfoResponse, ApproveUser
from wiki.wiki_api_client.enums import ResponsibilityType
from wiki.wiki_api_client.models import WikiApiClient
from wiki.wiki_api_client.repository import WikiApiClientRepository
from wiki.wiki_api_client.schemas import CreateWikiApiClient, WikiApiClientInfoResponse

admins_router = APIRouter()


@admins_router.post(
    "/approve_user",
    response_model=UserInfoResponse,
    status_code=status.HTTP_200_OK,
    summary="Approve the user for access to the system"
)
async def approve_user(
        approval_user: ApproveUser,
        user: WikiUserHandlerData = Depends(BasePermission(responsibility=ResponsibilityType.ADMIN)),
        session: AsyncSession = Depends(get_db)
):
    user_repository: UserRepository = UserRepository(session)
    api_client_repository: WikiApiClientRepository = WikiApiClientRepository(session)
    user_db: User = await user_repository.get_user_by_id(approval_user.user_id)
    if user_db.wiki_api_client_id is not None:
        api_client: WikiApiClient = await api_client_repository.get_wiki_api_client_by_id(user_db.wiki_api_client_id)
        raise WikiException(
            message=f"User already approve. Its WikiApiClient is in the {'enable' if api_client.is_enabled else 'disable'} state.",
            error_code=WikiErrorCode.USER_NOT_SPECIFIED,
            http_status_code=status.HTTP_409_CONFLICT
        )
    new_api_client_db: WikiApiClient = await api_client_repository.create_wiki_api_client(CreateWikiApiClient(
        description=approval_user.api_client_description,
        responsibility=approval_user.responsibility,
        is_enabled=True
    ))
    updated_user: User = await user_repository.update_user(user_db.id,
                                                           is_enabled=True,
                                                           is_user_agreement_accepted=True,
                                                           is_verified_email=True,
                                                           wiki_api_client_id=new_api_client_db.id)

    organization_response: Optional[OrganizationInfoResponse] = None
    if user.organization_id is not None:
        organization_repository: OrganizationRepository = OrganizationRepository(session)
        organization: Organization = await organization_repository.get_organization_by_id(user_db.organization_id)
        organization_response = OrganizationInfoResponse(
            id=organization.id,
            name=organization.name,
            description=organization.description,
            access=organization.access
        )

    wiki_api_client_response = WikiApiClientInfoResponse(
        id=new_api_client_db.id,
        description=new_api_client_db.description,
        responsibility=new_api_client_db.responsibility,
        is_enabled=new_api_client_db.is_enabled
    )

    return UserInfoResponse(
        email=user_db.email,
        username=user_db.username,
        first_name=user_db.first_name,
        last_name=user_db.last_name,
        second_name=user_db.second_name,
        position=user_db.position,
        is_user_agreement_accepted=user_db.is_user_agreement_accepted,
        is_verified_email=user_db.is_verified_email,
        is_enabled=user_db.is_enabled,
        organization=organization_response,
        wiki_api_client=wiki_api_client_response
    )
