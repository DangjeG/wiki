from typing import Optional

from fastapi import Security, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, APIKeyQuery, APIKeyHeader, APIKeyCookie
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from wiki.auth.authenticators.api_key import ApiKeyAuthenticatorInterface
from wiki.auth.authenticators.wiki_token import WikiTokenAuthenticatorInterface
from wiki.auth.schemas import UserHandlerData
from wiki.common.exceptions import WikiException, WikiErrorCode
from wiki.config import settings
from wiki.database.deps import get_db


wiki_api_key_query = APIKeyQuery(name=settings.AUTH_API_KEY_QUERY_NAME,
                                 scheme_name="WikiApiKey",
                                 auto_error=False)
wiki_api_key_header = APIKeyHeader(name=settings.AUTH_API_KEY_HEADER_NAME,
                                   scheme_name="WikiApiKey",
                                   auto_error=False)

wiki_access_token_cookie = APIKeyCookie(name=settings.AUTH_ACCESS_TOKEN_COOKIE_NAME,
                                        scheme_name="WikiAccessToken",
                                        auto_error=False)
wiki_access_token_bearer = HTTPBearer(scheme_name="WikiBearer", auto_error=False)
# wiki_refresh_token_cookie = APIKeyCookie(name=settings.AUTH_REFRESH_TOKEN_COOKIE_NAME,
#                                          scheme_name="WikiRefreshToken",
#                                          auto_error=False)


async def get_user(
        api_key_query: Optional[str] = Security(wiki_api_key_query),
        api_key_header: Optional[str] = Security(wiki_api_key_header),
        access_token_cookie: Optional[str] = Security(wiki_access_token_cookie),
        access_token_bearer: Optional[HTTPAuthorizationCredentials] = Security(wiki_access_token_bearer),
        session: AsyncSession = Depends(get_db)
) -> UserHandlerData:
    if api_key_query is not None or api_key_header is not None:
        authenticator = ApiKeyAuthenticatorInterface(session)
        return await authenticator.validate(api_key_query or api_key_header)
    if access_token_cookie is not None or access_token_bearer is not None:
        if access_token_bearer is not None:
            if not access_token_bearer.scheme == "Bearer":
                raise WikiException(
                    message="Invalid authentication scheme.",
                    error_code=WikiErrorCode.AUTH_NOT_VALIDATE_CREDENTIALS,
                    http_status_code=status.HTTP_403_FORBIDDEN
                )
        authenticator = WikiTokenAuthenticatorInterface(session)
        return await authenticator.validate(access_token_cookie or access_token_bearer.credentials)

    raise WikiException(message="Could not validate credentials.",
                        error_code=WikiErrorCode.AUTH_NOT_VALIDATE_CREDENTIALS,
                        http_status_code=status.HTTP_401_UNAUTHORIZED)
