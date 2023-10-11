from sqlalchemy.ext.asyncio import AsyncSession


class Resolver:
    session: AsyncSession

    def __init__(self, session: AsyncSession):
        self.session = session

    async def resolve(self, candidate):
        pass
