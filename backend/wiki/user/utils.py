from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from wiki.common.schemas import WikiUserHandlerData
from wiki.organization.models import Organization
from wiki.organization.repository import OrganizationRepository
from wiki.organization.schemas import OrganizationInfoResponse
from wiki.user.models import User
from wiki.user.repository import UserRepository
from wiki.user.schemas import UserInfoResponse
from wiki.wiki_api_client.models import WikiApiClient
from wiki.wiki_api_client.repository import WikiApiClientRepository
from wiki.wiki_api_client.schemas import WikiApiClientInfoResponse


async def get_user_info(user: User, session: AsyncSession) -> UserInfoResponse:
    wiki_api_client_response: Optional[WikiApiClientRepository] = None
    if user.wiki_api_client_id is not None:
        wiki_api_client_repository: WikiApiClientRepository = WikiApiClientRepository(session)
        wiki_api_client: WikiApiClient = await wiki_api_client_repository.get_wiki_api_client_by_id(
            user.wiki_api_client_id)
        wiki_api_client_response = WikiApiClientInfoResponse(
            id=wiki_api_client.id,
            description=wiki_api_client.description,
            responsibility=wiki_api_client.responsibility,
            is_enabled=wiki_api_client.is_enabled
        )

    organization_response: Optional[OrganizationInfoResponse] = None
    if user.organization_id is not None:
        organization_repository: OrganizationRepository = OrganizationRepository(session)
        organization: Organization = await organization_repository.get_organization_by_id(user.organization_id)
        organization_response = OrganizationInfoResponse(
            id=organization.id,
            name=organization.name,
            description=organization.description,
            access=organization.access
        )

    return UserInfoResponse(
        email=user.email,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        second_name=user.second_name,
        position=user.position,
        is_user_agreement_accepted=user.is_user_agreement_accepted,
        is_verified_email=user.is_verified_email,
        is_enabled=user.is_enabled,
        organization=organization_response,
        wiki_api_client=wiki_api_client_response
    )


async def get_user_info_by_handler_data(user: WikiUserHandlerData, session: AsyncSession) -> UserInfoResponse:
    user_repository: UserRepository = UserRepository(session)
    user_db = await user_repository.get_user_by_id(user.id)
    return await get_user_info(user_db, session)
