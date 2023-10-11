from typing import Optional
from uuid import UUID

from pydantic import EmailStr

from wiki.models import WikiBase
from wiki.wiki_api_client.enums import ResponsibilityType


class CreateUser(WikiBase):
    email: EmailStr
    username: str
    display_name: Optional[str] = None
    first_name: str
    last_name: str
    second_name: Optional[str] = None
    user_position: Optional[str] = None
    is_user_agreement_accepted: bool = False
    organization_id: UUID


class UserIdentifiers(WikiBase):
    user_id: Optional[UUID] = None
    user_name: Optional[str] = None
    email: Optional[EmailStr] = None


class UserInfoResponse(WikiBase):
    user_name: Optional[str] = None
    email: str
    first_name: str
    last_name: str
    second_name: Optional[str] = None
    responsibility: ResponsibilityType


class UserUpdate(WikiBase):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    display_name: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    second_name: Optional[str] = None
    user_position: Optional[str] = None
    organization_id: Optional[UUID] = None
    wiki_api_client_id: Optional[UUID] = None
