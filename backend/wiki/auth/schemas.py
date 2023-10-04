from enum import Enum

from pydantic import BaseModel, EmailStr

from wiki.config import settings


class UserLogin(BaseModel):
    email: EmailStr


class WikiTokenType(str, Enum):
    verify = "verify"
    access = "access"
    refresh = "refresh"


class VerifyTokenData(BaseModel):
    email: EmailStr
    user_ip: str
    user_agent: str


class AccessTokenData(BaseModel):
    email: EmailStr


class UserLoginResponse(BaseModel):
    email_to: EmailStr
    expire_minutes: int = settings.AUTH_VERIFY_TOKEN_EXPIRE_MINUTES
    verify_token: str


class UserVerifyResponse(BaseModel):
    access_token: str


class VerifyData(BaseModel):
    token: str
    code: int
