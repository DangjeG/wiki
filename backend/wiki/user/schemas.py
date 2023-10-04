from typing import Optional

from pydantic import BaseModel, EmailStr


class CreateUser(BaseModel):
    email: EmailStr
    username: str
    display_name: Optional[str] = None
    first_name: str
    last_name: str
    second_name: Optional[str] = None
    is_trusted: bool = False
