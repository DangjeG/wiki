from typing import Optional

from pydantic import EmailStr

from wiki.auth.enums import VerificationType
from wiki.config import settings
from wiki.models import WikiBase


class FrontendUserLogin(WikiBase):
    email: Optional[EmailStr] = None
    username:  Optional[str] = None


class BaseTokenData(WikiBase):
    email: EmailStr


class AccessTokenData(BaseTokenData):
    api_client_id: str


class VerifyTokenData(BaseTokenData):
    user_ip: str
    user_agent: str
    appointment: VerificationType


class UserSignResponse(WikiBase):
    email_to: EmailStr
    expire_minutes: int = settings.AUTH_VERIFY_TOKEN_EXPIRE_MINUTES
    verify_token: str


class VerifyData(WikiBase):
    token: str
    verification_code: int
