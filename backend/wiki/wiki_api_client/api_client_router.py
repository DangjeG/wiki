from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from wiki.common.schemas import WikiUserHandlerData
from wiki.database.deps import get_db
from wiki.permissions.base import BasePermission
from wiki.wiki_api_client.enums import ResponsibilityType
from wiki.wiki_api_client.models import WikiApiClient
from wiki.wiki_api_client.repository import WikiApiClientRepository
from wiki.wiki_api_client.schemas import WikiApiClientInfoResponse, UpdateWikiApiClient

wiki_api_client_router = APIRouter()


@wiki_api_client_router.put(
    "/",
    response_model=WikiApiClientInfoResponse,
    status_code=status.HTTP_200_OK,
    summary="Update wiki api client"
)
async def update_wiki_api_client(
        wiki_api_client_id: UUID,
        user: WikiUserHandlerData = Depends(BasePermission(responsibility=ResponsibilityType.ADMIN)),
        upd_wiki_api_client: UpdateWikiApiClient = Depends(),
        session: AsyncSession = Depends(get_db)
):
    client_repository: WikiApiClientRepository = WikiApiClientRepository(session)

    await client_repository.update_wiki_api_client(
        wiki_api_client_id,
        description=upd_wiki_api_client.description,
        responsibility=upd_wiki_api_client.responsibility,
        is_enabled=upd_wiki_api_client.is_enabled
    )

    wiki_api_client_info_response: WikiApiClient =\
        await client_repository.get_wiki_api_client_by_id(wiki_api_client_id)

    return WikiApiClientInfoResponse(
        description=wiki_api_client_info_response.description,
        responsibility=wiki_api_client_info_response.responsibility,
        is_enabled=wiki_api_client_info_response.is_enabled
    )
