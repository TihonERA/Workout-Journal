from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.history_analytics.domain.training_day_history import TrainingDayHistory
from src.history_analytics.infrastructure.mappers.training_day_history_mapper import (
    TrainingDayHistoryMapper,
)
from src.history_analytics.infrastructure.models.training_day_history import (
    TrainingDayHistoryModel,
)


class TrainingDayHistoryRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, id: int) -> TrainingDayHistory | None:
        training_day_history = await self.session.get(
            TrainingDayHistory, id, with_for_update=True
        )

        if training_day_history is None:
            return None

        return TrainingDayHistoryMapper.to_domain(training_day_history)

    async def create(
        self, training_day_history: TrainingDayHistory
    ) -> TrainingDayHistory:
        training_day_history_model = TrainingDayHistoryMapper.to_orm(
            training_day_history
        )

        self.session.add(training_day_history_model)
        await self.session.flush()

        return TrainingDayHistoryMapper.to_domain(training_day_history_model)

    async def delete(self, id: int) -> None:
        stmt = delete(TrainingDayHistoryModel).where(TrainingDayHistoryModel.id == id)

        await self.session.execute(stmt)
        await self.session.flush()
