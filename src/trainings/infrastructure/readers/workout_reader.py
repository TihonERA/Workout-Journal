from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.trainings.application.dto.workout import WorkoutReadDTO
from src.trainings.infrastructure.mappers.workout_mapper import WorkoutMapper
from src.trainings.infrastructure.models.workout import WorkoutModel


class WorkoutReader:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, id: int) -> WorkoutReadDTO | None:
        workout = await self.session.get(
            WorkoutModel, id, options=[selectinload(WorkoutModel.training_days)]
        )

        if workout is None:
            return None

        return WorkoutMapper.to_dto(workout)
