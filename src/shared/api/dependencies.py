from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import async_session_factory
from src.shared.application.ports import IUnitOfWork
from src.shared.infrastructure.repositories.unit_of_work import UnitOfWork


def get_uow() -> IUnitOfWork:
    return UnitOfWork(async_session_factory)


async def get_db_session() -> AsyncGenerator[AsyncSession]:
    async with async_session_factory() as session:
        try:
            yield session
        finally:
            await session.close()
