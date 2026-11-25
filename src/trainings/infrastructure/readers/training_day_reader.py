from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.trainings.application.dto.training_day import TrainingDayReadDTO
from src.trainings.infrastructure.mappers.training_day_mapper import (
    TrainingDayMapper,
)
from src.trainings.infrastructure.models.trainingday import TrainingDayModel


class TrainingDayReader:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, id: int) -> TrainingDayReadDTO | None:
        training_day = await self.session.get(
            TrainingDayModel,
            id,
            options=[selectinload(TrainingDayModel.day_exercises)],
        )

        if training_day is None:
            return None

        return TrainingDayMapper.to_dto(training_day)
