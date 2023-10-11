from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from wiki.auth.authenticators.api_key import ApiKeyAuthenticatorInterface
from wiki.common.schemas import BaseResponse, WikiUserHandlerData
from wiki.database.deps import get_db
from wiki.permissions.base import BasePermission
from wiki.wiki_api_client.enums import ResponsibilityType
from wiki.wiki_api_client.repository import WikiApiClientRepository
from wiki.wiki_api_client.schemas import (
    WikiApiKeyInfoResponse,
    CreateWikiApiKey
)

wiki_api_key_router = APIRouter()


@wiki_api_key_router.post(
    "/",
    response_model=WikiApiKeyInfoResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Create wiki api key"
)
async def create_wiki_api_key(
        expires_date: datetime,
        user: WikiUserHandlerData = Depends(BasePermission(responsibility=ResponsibilityType.VIEWER)),
        session: AsyncSession = Depends(get_db)
):
    client_repository: WikiApiClientRepository = WikiApiClientRepository(session)

    api_key = ApiKeyAuthenticatorInterface.generate_api_key()
    api_key_prefix = api_key[:8]
    api_key_hash = ApiKeyAuthenticatorInterface.get_api_key_hash(api_key)

    await client_repository.create_wiki_api_key(
        CreateWikiApiKey(
            api_key_hash=api_key_hash,
            api_key_prefix=api_key_prefix,
            expires_date=expires_date,
            owner_id=user.wiki_api_client.id
        )
    )

    return WikiApiKeyInfoResponse(
        api_key=api_key,
        expires_date=expires_date,
        create_date=datetime.now(),
        api_key_prefix=api_key_prefix
    )


@wiki_api_key_router.delete(
    "/",
    response_model=BaseResponse,
    status_code=status.HTTP_200_OK,
    summary="Delete wiki api key"
)
async def delete_wiki_api_key(
        api_key_id: UUID,
        user: WikiUserHandlerData = Depends(BasePermission(responsibility=ResponsibilityType.VIEWER)),
        session: AsyncSession = Depends(get_db)
):
    client_repository: WikiApiClientRepository = WikiApiClientRepository(session)

    await client_repository.mark_wiki_api_key_deleted(api_key_id)

    return BaseResponse(
        msg="Key deleted"
    )


@wiki_api_key_router.put(
    "/deactivate",
    response_model=BaseResponse,
    status_code=status.HTTP_200_OK,
    summary="Deactivate wiki api key"
)
async def deactivate_wiki_api_key(
        api_key_id: UUID,
        user: WikiUserHandlerData = Depends(BasePermission(responsibility=ResponsibilityType.VIEWER)),
        session: AsyncSession = Depends(get_db)):
    client_repository: WikiApiClientRepository = WikiApiClientRepository(session)

    await client_repository.deactivate_wiki_api_key(api_key_id)

    return BaseResponse(
        msg="Key deactivated"
    )
