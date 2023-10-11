from typing import Optional
from uuid import UUID

from sqlalchemy import select, and_
from starlette import status

from wiki.common.exceptions import WikiException, WikiErrorCode
from wiki.database.repository import BaseRepository
from wiki.database.utils import menage_db_not_found_resul_method, NotFoundResultMode, menage_db_commit_method, \
    CommitMode
from wiki.wiki_api_client.enums import ResponsibilityType
from wiki.wiki_api_client.models import WikiApiClient, WikiApiKey
from wiki.wiki_api_client.schemas import CreateWikiApiClient, CreateWikiApiKey


class WikiApiClientRepository(BaseRepository):
    _api_client_not_found_exception = WikiException(
        message="Wiki api client not found.",
        error_code=WikiErrorCode.API_CLIENT_NOT_FOUND,
        http_status_code=status.HTTP_404_NOT_FOUND
    )
    _api_key_not_found_exception = WikiException(
        message="Wiki api key not found.",
        error_code=WikiErrorCode.API_KEY_NOT_FOUND,
        http_status_code=status.HTTP_404_NOT_FOUND
    )
    _api_key_hash_not_found_exception = WikiException(
        message="API key is not valid or expired.",
        error_code=WikiErrorCode.AUTH_API_KEY_NOT_VALID_OR_EXPIRED,
        http_status_code=status.HTTP_403_FORBIDDEN
    )

    @menage_db_not_found_resul_method(NotFoundResultMode.EXCEPTION, ex=_api_client_not_found_exception)
    async def get_wiki_api_client_by_id(self, api_client_id: UUID) -> WikiApiClient:
        api_client_query = await self.session.get(WikiApiClient, api_client_id)
        return api_client_query

    async def get_all_wiki_api_clients(self) -> list[WikiApiClient]:
        api_client_query = await self.session.execute(select(WikiApiClient))
        res = api_client_query.scalars().all()
        return res

    @menage_db_not_found_resul_method(NotFoundResultMode.EXCEPTION, ex=_api_key_not_found_exception)
    async def get_wiki_api_key_by_id(self, api_key_id: UUID) -> WikiApiKey:
        api_key_query = await self.session.get(WikiApiKey, api_key_id)
        return api_key_query

    @menage_db_not_found_resul_method(NotFoundResultMode.EXCEPTION, ex=_api_key_hash_not_found_exception)
    async def get_wiki_api_key_by_key_hash(self, api_key_hash) -> WikiApiKey:
        st = select(WikiApiKey).where(WikiApiKey.api_key_hash == api_key_hash)
        res = (await self.session.execute(st)).scalar()
        return res

    async def get_wiki_api_keys_for_api_client(self,
                                               api_client_id: UUID,
                                               *,
                                               is_with_deleted: bool = False) -> list[WikiApiKey]:
        whereclause = [WikiApiKey.owner_id == api_client_id]
        if not is_with_deleted:
            whereclause.append(WikiApiKey.is_deleted == False)
        st = select(WikiApiKey).where(and_(*whereclause))
        res = (await self.session.execute(st)).scalars().all()
        return res

    @menage_db_commit_method(CommitMode.COMMIT)
    async def create_wiki_api_key(self, create_wiki_api_key: CreateWikiApiKey) -> WikiApiKey:
        new_api_key = WikiApiKey(
            api_key_hash=create_wiki_api_key.api_key_hash,
            api_key_prefix=create_wiki_api_key.api_key_prefix,
            expires_date=create_wiki_api_key.expires_date,
            owner_id=create_wiki_api_key.owner_id
        )

        self.session.add(new_api_key)

        return new_api_key

    @menage_db_commit_method(CommitMode.FLUSH)
    async def deactivate_wiki_api_key(self, api_key_id: UUID) -> WikiApiKey:
        api_key: WikiApiKey = await self.get_wiki_api_key_by_id(api_key_id)
        api_key.is_enabled = False

        self.session.add(api_key)

    @menage_db_commit_method(CommitMode.FLUSH)
    async def mark_wiki_api_key_deleted(self, api_key_id: UUID) -> None:
        api_key: WikiApiKey = await self.get_wiki_api_key_by_id(api_key_id)
        api_key.is_deleted = True

        self.session.add(api_key)

    @menage_db_commit_method(CommitMode.COMMIT)
    async def create_wiki_api_client(self, create_api_client: CreateWikiApiClient) -> WikiApiClient:
        new_api_client = WikiApiClient(
            description=create_api_client.description,
            responsibility=create_api_client.responsibility,
            is_enabled=create_api_client.is_enabled
        )

        self.session.add(new_api_client)

        return new_api_client

    @menage_db_commit_method(CommitMode.FLUSH)
    async def update_wiki_api_client(self,
                                     api_client_id: UUID,
                                     *,
                                     description: Optional[str] = None,
                                     responsibility: Optional[ResponsibilityType] = None,
                                     is_enabled: Optional[bool] = None):
        api_client: WikiApiClient = await self.get_wiki_api_client_by_id(api_client_id)
        if description is not None:
            api_client.description = description
        if responsibility is not None:
            api_client.responsibility = responsibility
        if is_enabled is not None:
            api_client.is_enabled = is_enabled

        self.session.add(api_client)

        return api_client

    @menage_db_commit_method(CommitMode.COMMIT)
    async def mark_wiki_api_client_deleted(self, api_client_id: UUID) -> None:
        api_client: WikiApiClient = await self.get_wiki_api_client_by_id(api_client_id)
        api_client.is_deleted = True
        api_client.is_enabled = False

        self.session.add(api_client)
