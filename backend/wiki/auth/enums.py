from enum import StrEnum


class AuthorizationMode(StrEnum):
    UNAUTHORIZED = "UNAUTHORIZED"
    AUTHORIZED = "AUTHORIZED"


class VerificationType(StrEnum):
    signup = "signup"
    login = "login"
