from enum import IntEnum, Enum


class AuthorizationMode(IntEnum):
    UNAUTHORIZED = 0
    AUTHORIZED = 10


class VerificationType(str, Enum):
    signup = "signup"
    login = "login"
