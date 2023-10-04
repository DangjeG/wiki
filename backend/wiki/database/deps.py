from sqlalchemy.ext.asyncio import AsyncSession

from wiki.database.core import get_session


async def get_db():
    session: AsyncSession = get_session()
    with session.begin() as transaction:
        yield session
