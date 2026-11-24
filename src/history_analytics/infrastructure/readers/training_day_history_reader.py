from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.history_analytics.application.dto.training_day_history import (
    TrainingDayHistoryDetailDTO,
)
from src.history_analytics.infrastructure.mappers.training_day_history_mapper import (
    TrainingDayHistoryMapper,
)
from src.history_analytics.infrastructure.models.exercise_history import (
    ExerciseHistoryModel,
)
from src.history_analytics.infrastructure.models.training_day_history import (
    TrainingDayHistoryModel,
)


class TrainingDayHistoryReader:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_loaded(self, id: int) -> TrainingDayHistoryDetailDTO | None:
        training_day_history = await self.session.get(
            TrainingDayHistoryModel,
            id,
            options=[
                selectinload(TrainingDayHistoryModel.exercises_history).selectinload(
                    ExerciseHistoryModel.sets_history
                )
            ],
        )

        if training_day_history is None:
            return None

        return TrainingDayHistoryMapper.to_dto(training_day_history)
