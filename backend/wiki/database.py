from sqlalchemy.ext.asyncio import create_async_engine
from wiki.config import settings

engine = create_async_engine(settings.get_db_url())
