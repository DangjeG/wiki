import time
from datetime import timedelta, datetime
from random import randrange

from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

from wiki.auth.schemas import VerifyTokenData, AccessTokenData
from wiki.config import settings


class WikiBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(WikiBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(WikiBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            payload: dict = self.verify_token(credentials.credentials)
            if not payload:
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return payload
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    @classmethod
    def verify_token(cls, token: str) -> dict:
        token_sep = token.find(settings.AUTH_TOKEN_SEPARATOR)
        prefix: str = token[:token_sep]
        jwt_token: str = token[token_sep + 1:]
        return cls.decode_token(jwt_token, settings.AUTH_SECRET)

    @classmethod
    def verify_verification_token(cls, token: str, code: int) -> dict:
        token_sep = token.find(settings.AUTH_TOKEN_SEPARATOR)
        prefix: str = token[:token_sep]
        jwt_token: str = token[token_sep + 1:]
        return cls.decode_token(jwt_token, _get_verify_token_secret(code))

    @classmethod
    def decode_token(cls, token: str, secret: str | dict) -> dict:
        try:
            decoded_token: dict = jwt.decode(token, secret, algorithms=settings.AUTH_ALGORITHM)
            if decoded_token["exp"] >= time.time():
                return decoded_token
            else:
                return None
        except JWTError:
            return None


def create_verify_token(data: VerifyTokenData) -> tuple[int, str]:
    verification_code: int = randrange(100000, 999999)
    encoded_jwt = jwt.encode(_get_token_claims(data.model_dump(), settings.AUTH_VERIFY_TOKEN_EXPIRE_MINUTES),
                             _get_verify_token_secret(verification_code),
                             algorithm=settings.AUTH_ALGORITHM)
    return verification_code, f"{settings.AUTH_VERIFY_TOKEN_PREFIX}{settings.AUTH_TOKEN_SEPARATOR}{encoded_jwt}"


def create_access_token(data: AccessTokenData) -> str:
    encoded_jwt = jwt.encode(_get_token_claims(data.model_dump(), settings.AUTH_ACCESS_TOKEN_EXPIRE_MINUTES),
                             settings.AUTH_SECRET,
                             algorithm=settings.AUTH_ALGORITHM)
    return f"{settings.AUTH_ACCESS_TOKEN_PREFIX}{settings.AUTH_TOKEN_SEPARATOR}{encoded_jwt}"


def _get_token_claims(data: dict, expire_minutes: int):
    expires_delta = timedelta(minutes=expire_minutes)
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return to_encode


def _get_verify_token_secret(verification_code: int) -> dict:
    return f"{settings.AUTH_SECRET}_{verification_code}"
