from functools import lru_cache

from lakefs_client import Configuration

from wiki.config import settings


@lru_cache
def get_configuration() -> Configuration:
    return Configuration(
        host=settings.LAKECTL_SERVER_ENDPOINT_URL,
        username=settings.LAKEFS_INSTALLATION_ACCESS_KEY_ID,
        password=settings.LAKEFS_INSTALLATION_SECRET_ACCESS_KEY
    )


configuration: Configuration = get_configuration()
