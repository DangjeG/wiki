from random import randrange
from typing import Optional

from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from wiki.auth.authenticators.base import AuthenticatorType, BaseTokenAuthenticatorInterface
from wiki.auth.schemas import VerifyTokenData, VerificationType
from wiki.common.exceptions import WikiException, WikiErrorCode
from wiki.common.schemas import WikiUserHandlerData
from wiki.config import settings


class VerificationCodeAuthenticatorInterface(BaseTokenAuthenticatorInterface):
    code_length: int = 6
    verification_code: int

    def __init__(self,
                 session: AsyncSession,
                 *,
                 verification_code: Optional[int] = None,
                 code_length: int = 6):
        super().__init__(session)
        self.code_length = code_length
        if verification_code is not None:
            self.verification_code = verification_code
        else:
            self.verification_code = self.generate_verification_code()
        self.authenticator_type = AuthenticatorType.verification_code

    def generate_verification_code(self):
        code = randrange(10 ** (self.code_length - 1), 10 ** self.code_length - 1)
        self.verification_code = code
        return code

    @classmethod
    async def verify_verification_token(cls, token: str, verification_code: int) -> str:
        payload = cls.decode_jwt_token(token, cls._get_secret(verification_code))
        ex = WikiException(
            message="Token is not valid or expired.",
            error_code=WikiErrorCode.AUTH_TOKEN_NOT_VALID_OR_EXPIRED,
            http_status_code=status.HTTP_403_FORBIDDEN
        )
        if payload is None:
            raise ex
        email = payload.get("email")
        appointment = payload.get("appointment")
        if email is None or appointment is None:
            raise ex

        return email, appointment

    @classmethod
    def _get_secret(cls, verification_code: int) -> str:
        return f"{settings.AUTH_SECRET_VERIFY}_{verification_code}"

    @classmethod
    def create_verify_token(cls, data: VerifyTokenData, verification_code: int) -> str:
        encoded_jwt = jwt.encode(cls._get_token_claims(data.model_dump(), settings.AUTH_VERIFY_TOKEN_EXPIRE_MINUTES),
                                 cls._get_secret(verification_code),
                                 algorithm=settings.AUTH_ALGORITHM)
        return encoded_jwt

    async def validate(self, credentials) -> WikiUserHandlerData | str:
        email, appointment = await self.verify_verification_token(credentials, self.verification_code)

        appointment: VerificationType
        match appointment:
            case VerificationType.signup:
                return email
            case VerificationType.login:
                user = await self.user_repository.get_user_by_email(email)
                api_client = await self.verify_api_client(user.wiki_api_client_id)
                user, organization = await self.verify_user(api_client)
                if not user.is_verified_email:
                    user = await self.user_repository.update_user(user.id, is_verified_email=True)

                return WikiUserHandlerData(
                    id=user.id,
                    email=user.email,
                    username=user.username,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    second_name=user.second_name,
                    position=user.position,
                    organization=organization,
                    wiki_api_client=api_client
                )

        raise WikiException(
            message="Invalid verification type.",
            error_code=WikiErrorCode.GENERIC_ERROR,
            http_status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
