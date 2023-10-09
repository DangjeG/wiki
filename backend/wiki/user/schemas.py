from typing import Optional
from uuid import UUID

from pydantic import EmailStr

from wiki.models import WikiBase


class CreateUser(WikiBase):
    email: EmailStr
    username: str
    display_name: Optional[str] = None
    first_name: str
    last_name: str
    second_name: Optional[str] = None
    position: Optional[str] = None,
    organization_id: Optional[UUID] = None
