from types import TracebackType
from typing import Self, Type

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.trainings.infrastructure.repositories.training_day_repository import (
    TrainingDayRepository,
)
from src.trainings.infrastructure.repositories.workout_repository import (
    WorkoutRepository,
)


class UnitOfWork:
    def __init__(self, async_sessionmaker: async_sessionmaker[AsyncSession]) -> None:
        self.async_sessionmaker = async_sessionmaker

    async def __aenter__(self) -> Self:
        self.session = self.async_sessionmaker()

        self.workout_repo = WorkoutRepository(self.session)
        self.tr_day_repo = TrainingDayRepository(self.session)

        return self

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        try:
            if exc_type is not None:
                await self.rollback()
        finally:
            await self.session.close()

    async def rollback(self) -> None:
        await self.session.rollback()

    async def commit(self) -> None:
        await self.session.commit()
