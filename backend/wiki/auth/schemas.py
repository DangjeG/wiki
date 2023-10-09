from enum import Enum
from typing import Optional, TypedDict
from uuid import UUID

from pydantic import EmailStr

from wiki.config import settings
from wiki.models import WikiBase
from wiki.organization.models import Organization
from wiki.wiki_api_client.models import WikiApiClient


class FrontendUserLogin(WikiBase):
    email: Optional[EmailStr] = None
    username:  Optional[str] = None


class BaseTokenData(WikiBase):
    email: EmailStr


class AccessTokenData(BaseTokenData):
    api_client_id: str


class VerificationType(str, Enum):
    signup = "signup"
    login = "login"


class VerifyTokenData(BaseTokenData):
    user_ip: str
    user_agent: str
    appointment: VerificationType


class UserSignResponse(WikiBase):
    email_to: EmailStr
    expire_minutes: int = settings.AUTH_VERIFY_TOKEN_EXPIRE_MINUTES
    verify_token: str


# class FrontendUserSignup(WikiBase):
#     email: EmailStr
#     username: Optional[str]
#     display_name: Optional[str]
#     first_name: str
#     last_name: str
#     second_name: str
#     position: Optional[str]
#     is_user_agreement_accepted: bool
#     organization_id: UUID


# class UserVerifyResponse(WikiBase):
#     access_token: str


class VerifyData(WikiBase):
    token: str
    verification_code: int


class UserHandlerData(WikiBase):
    id: UUID
    email: str
    username: Optional[str] = None
    display_name: Optional[str] = None
    first_name: str
    last_name: str
    second_name: Optional[str] = None
    position: Optional[str] = None
    organization: Optional[Organization] = None
    wiki_api_client: Optional[WikiApiClient] = None
