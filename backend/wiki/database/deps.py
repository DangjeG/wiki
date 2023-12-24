from sqlalchemy.ext.asyncio import AsyncSession

from wiki.database.core import get_session, Base, engine


async def get_db():
    session: AsyncSession = get_session()
    async with session.begin() as transaction:
        yield session


async def db_metadata_create_all():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
