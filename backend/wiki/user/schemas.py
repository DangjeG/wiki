from typing import Optional
from uuid import UUID

from pydantic import EmailStr

from wiki.models import WikiBase
from wiki.organization.schemas import OrganizationInfoResponse
from wiki.wiki_api_client.enums import ResponsibilityType
from wiki.wiki_api_client.schemas import WikiApiClientInfoResponse, CreateWikiApiClient


class CreateUser(WikiBase):
    email: EmailStr
    username: str
    first_name: str
    last_name: str
    second_name: Optional[str] = None
    position: Optional[str] = None
    is_user_agreement_accepted: bool = False
    organization_id: UUID


class CreateVerifiedUser(WikiBase):
    email: EmailStr
    username: Optional[str] = None
    first_name: str
    last_name: str
    second_name: Optional[str] = None
    position: Optional[str] = None
    is_user_agreement_accepted: bool = True
    is_verified_email: bool = True
    is_enabled: bool = True
    organization_id: UUID
    wiki_api_client: CreateWikiApiClient


class ApproveUser(WikiBase):
    responsibility: ResponsibilityType
    api_client_description: Optional[str] = None


class UserIdentifiers(WikiBase):
    user_id: Optional[UUID] = None
    username: Optional[str] = None
    email: Optional[EmailStr] = None


class UserBaseInfoResponse(WikiBase):
    email: EmailStr
    username: Optional[str] = None
    first_name: str
    last_name: str
    second_name: Optional[str] = None
    position: Optional[str] = None
    organization: OrganizationInfoResponse
    wiki_api_client: Optional[WikiApiClientInfoResponse] = None


class UserFullInfoResponse(UserBaseInfoResponse):
    is_user_agreement_accepted: bool
    is_verified_email: bool
    is_enabled: bool


class UserUpdate(WikiBase):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    second_name: Optional[str] = None
    position: Optional[str] = None
    organization_id: Optional[UUID] = None
    is_enabled: Optional[bool] = None
    is_user_agreement_accepted: Optional[bool] = None
    is_verified_email: Optional[bool] = None
    wiki_api_client_id: Optional[UUID] = None

class UserFilter(WikiBase):
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    second_name: Optional[str] = None
