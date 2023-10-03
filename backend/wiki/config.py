import os
from enum import Enum
from functools import lru_cache

from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings


class EnvironmentType(str, Enum):
    DEV = "DEV"
    LOCAL = "LOCAL"
    PROD = "PROD"


class DbSchemaType(str, Enum):
    sqlite = "sqlite"
    postgresql = "postgresql"


class DbDriverType(str, Enum):
    aiosqlite = "aiosqlite"
    asyncpg = "asyncpg"


class Settings(BaseSettings):
    PROJECT_NAME: str = "Wiki"
    PROJECT_DESCRIPTION: str = "Welcome to Wiki's API documentation! Here you will able to discover all of the ways you can interact with the Wiki API."
    VERSION: str = "0.0.1"
    API_V1_STR: str = "/api/v1"

    ENVIRONMENT: EnvironmentType = EnvironmentType.DEV
    DB_ECHO: bool
    LOG_FILENAME: str = "wiki.log"

    DB_SCHEMA: DbSchemaType.sqlite
    DB_DRIVER: DbDriverType.aiosqlite
    DB_FILENAME: str = "wiki.db"
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_NAME: str = "wiki"

    DB_POOL_SIZE = 75
    DB_MAX_OVERFLOW = 20

    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []

    def get_db_url(self):
        if self.DB_SCHEMA == DbSchemaType.sqlite:
            return f"{self.DB_SCHEMA}+{self.DB_DRIVER}:///{os.path.join(os.getcwd(), self.DB_FILENAME)}"
        else:
            return f"{self.DB_SCHEMA}+{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings: Settings = get_settings()

