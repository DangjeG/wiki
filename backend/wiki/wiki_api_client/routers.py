import binascii
import os
from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from wiki.auth.authenticators.api_key import ApiKeyAuthenticatorInterface
from wiki.common.schemas import BaseResponse
from wiki.database.deps import get_db
from wiki.wiki_api_client.repository import WikiApiClientRepository
from wiki.wiki_api_client.schemas import WikiApiClientInfoResponse, UpdateWikiApiClient, WikiApiKeyInfoResponse, \
    CreateWikiApiKey

wiki_api_client_router = APIRouter()


@wiki_api_client_router.post(
    "/",
    response_model=WikiApiClientInfoResponse,
    status_code=status.HTTP_200_OK,
    description="Update wiki client api."
)
async def update_wiki_client_api(wiki_api_client_id: UUID,
                                 update_wiki_api_client: UpdateWikiApiClient = Depends(),
                                 session: AsyncSession = Depends(get_db)):
    client_repository: WikiApiClientRepository = WikiApiClientRepository(session)

    await client_repository.update_wiki_api_client(
        wiki_api_client_id,
        description=update_wiki_api_client.description,
        responsibility=update_wiki_api_client.responsibility,
        is_enabled=update_wiki_api_client.is_enabled
    )

    wiki_api_client_info_response = await client_repository.get_wiki_api_client_by_id(wiki_api_client_id)

    return WikiApiClientInfoResponse(
        description=wiki_api_client_info_response.description,
        responsibility=wiki_api_client_info_response.responsibility,
        is_enabled=wiki_api_client_info_response.description
    )


@wiki_api_client_router.post(
    "/",
    response_model=WikiApiKeyInfoResponse,
    status_code=status.HTTP_200_OK,
    description="Create wiki api key."
)
async def create_wiki_api_key(expires_date: datetime,
                              session: AsyncSession = Depends(get_db)):
    client_repository: WikiApiClientRepository = WikiApiClientRepository(session)

    api_key = binascii.b2a_hex(os.urandom(15)).decode(encoding="utf-8")

    api_key_prefix = api_key[:8]

    api_key_hash = ApiKeyAuthenticatorInterface.get_api_key_hash(api_key)

    await client_repository.create_wiki_api_key(
        CreateWikiApiKey(
            api_key_hash=api_key_hash,
            api_key_prefix=api_key_prefix,
            expires_date=expires_date,
            owner_id=""  # todo добавить owner
        )
    )

    return WikiApiKeyInfoResponse(
        api_key=api_key,
        expires_date=expires_date,
        create_date=datetime.now(),
        api_key_prefix=api_key_prefix
    )

@wiki_api_client_router.delete(
    "/",
    response_model=BaseResponse,
    status_code=status.HTTP_200_OK,
    description="Delete wiki api key."
)
async def delete_wiki_api_key(api_key_id: UUID,
                              session: AsyncSession = Depends(get_db)):
    client_repository: WikiApiClientRepository = WikiApiClientRepository(session)

    await client_repository.mark_wiki_api_key_deleted(api_key_id)

    return BaseResponse(
        msg="Key deleted"
    )

@wiki_api_client_router.post(
    "/deactivate",
    response_model=BaseResponse,
    status_code=status.HTTP_200_OK,
    description="Deactivate wiki api key."
)
async def deactivate_wiki_api_key(api_key_id: UUID,
                                  session: AsyncSession = Depends(get_db)):
    client_repository: WikiApiClientRepository = WikiApiClientRepository(session)

    await client_repository.deactivate_wiki_api_key(api_key_id)

    return BaseResponse(
        msg="Key deactivated"
    )
