from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from wiki.auth.enums import AuthorizationMode
from wiki.common.exceptions import WikiErrorCode
from wiki.models import WikiBase
from wiki.wiki_api_client.enums import ResponsibilityType
from wiki.wiki_api_client.models import WikiApiClient


class WikiErrorResponse(BaseModel):
    """The format of an error response from the Wiki API."""

    error_code: WikiErrorCode
    message: str


class BaseResponse(WikiBase):
    status: str = "success"
    msg: str = ""


class HealthCheck(WikiBase):
    """Response model to validate and return when performing a health check."""

    status: str = "OK"


class ExternalUserHandlerData(WikiBase):
    authorisation_status: AuthorizationMode = AuthorizationMode.UNAUTHORIZED


class FakeWikiApiClient(WikiBase):
    id: UUID
    description: str
    responsibility: ResponsibilityType = ResponsibilityType.ADMIN


class WikiUserHandlerData(ExternalUserHandlerData):
    authorisation_status: AuthorizationMode = AuthorizationMode.AUTHORIZED

    id: UUID
    email: str
    username: Optional[str] = None
    first_name: str
    last_name: str
    second_name: Optional[str] = None
    position: Optional[str] = None
    wiki_api_client: Optional[WikiApiClient | FakeWikiApiClient]
