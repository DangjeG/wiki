from yadisk_async import YaDisk

from wiki.config import settings


async def get_ya_disk_session_storage():
    async with YaDisk(token=settings.YA_OAUTH_TOKEN) as session:
        yield session
