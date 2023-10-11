from typing import Optional

from fastapi import Depends, Security
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from wiki.auth.deps import (
    AuthUserDependency,
    wiki_api_key_query,
    wiki_api_key_header,
    wiki_access_token_cookie,
    wiki_access_token_bearer
)
from wiki.auth.enums import AuthorizationMode
from wiki.common.exceptions import WikiException, WikiErrorCode
from wiki.common.schemas import ExternalUserHandlerData, WikiUserHandlerData
from wiki.database.deps import get_db
from wiki.wiki_api_client.enums import ResponsibilityType


class _ResponsibilityPermission(AuthUserDependency):
    responsibility: ResponsibilityType

    def __init__(self,
                 authorisation_mode: AuthorizationMode = AuthorizationMode.AUTHORIZED,
                 responsibility: ResponsibilityType = ResponsibilityType.ADMIN):
        super().__init__(authorisation_mode)
        self.responsibility = responsibility

    async def __call__(self,
                       api_key_query=None,
                       api_key_header=None,
                       access_token_cookie=None,
                       access_token_bearer=None,
                       session=None):
        # user: WikiUserHandlerData,
        user: ExternalUserHandlerData | WikiUserHandlerData = await super().__call__(
            api_key_query,
            api_key_header,
            access_token_cookie,
            access_token_bearer,
            session
        )

        if self.authorisation_mode != AuthorizationMode.UNAUTHORIZED:
            if not isinstance(user, WikiUserHandlerData) or self.responsibility > user.wiki_api_client.responsibility:
                raise WikiException(
                    message="You have insufficiently responsibility.",
                    error_code=WikiErrorCode.AUTH_INSUFFICIENTLY_RESPONSIBILITY,
                    http_status_code=status.HTTP_403_FORBIDDEN
                )

        return user


class BasePermission(_ResponsibilityPermission):
    """
    Base permission class. Note: if unauthorized mode is specified, responsibility will not be checked.
    """
    responsibility: ResponsibilityType

    async def __call__(
            self,
            api_key_query: Optional[str] = Security(wiki_api_key_query),
            api_key_header: Optional[str] = Security(wiki_api_key_header),
            access_token_cookie: Optional[str] = Security(wiki_access_token_cookie),
            access_token_bearer: Optional[HTTPAuthorizationCredentials] = Security(wiki_access_token_bearer),
            session: AsyncSession = Depends(get_db)
    ) -> ExternalUserHandlerData | WikiUserHandlerData:
        return super().__call__(api_key_query,
                                api_key_header,
                                access_token_cookie,
                                access_token_bearer,
                                session)
