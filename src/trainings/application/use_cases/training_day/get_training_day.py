from typing import Protocol
from uuid import UUID

from src.trainings.application.dto.training_day import TrainingDayReadDTO
from src.trainings.application.dto.workout import WorkoutReadDTO
from src.trainings.domain.exceptions.training_day_exceptions import (
    TrainingDayAccessDenied,
    TrainingDayNotFound,
)
from src.trainings.domain.exceptions.workout_exceptions import (
    WorkoutAccessDenied,
    WorkoutNotFound,
)


class TrainingDayReaderPort(Protocol):
    async def get(self, id: int) -> TrainingDayReadDTO | None: ...


class WorkoutReaderPort(Protocol):
    async def get(self, id: int) -> WorkoutReadDTO | None: ...


class GetTrainingDayUseCase:
    def __init__(
        self,
        workout_reader: WorkoutReaderPort,
        tr_day_reader: TrainingDayReaderPort,
    ) -> None:
        self._workout_reader = workout_reader
        self._tr_day_reader = tr_day_reader

    async def __call__(
        self, user_id: UUID, workout_id: int, day_id: int
    ) -> TrainingDayReadDTO:
        workout = await self._workout_reader.get(workout_id)

        if workout is None:
            raise WorkoutNotFound(workout_id)

        if not workout.public and workout.user_id != user_id:
            raise WorkoutAccessDenied()

        training_day = await self._tr_day_reader.get(day_id)

        if training_day is None:
            raise TrainingDayNotFound

        if training_day.workout_id != workout_id:
            raise TrainingDayAccessDenied()

        return training_day
