from typing import Protocol
from uuid import UUID

from src.trainings.application.dto.workout import WorkoutReadDTO
from src.trainings.domain.exceptions.workout_exceptions import (
    WorkoutAccessDenied,
    WorkoutNotFound,
)


class WorkoutReader(Protocol):
    async def get(self, id: int) -> WorkoutReadDTO | None: ...


class GetLoadedWorkoutUseCase:
    def __init__(self, workout_reader: WorkoutReader) -> None:
        self._workout_reader = workout_reader

    async def __call__(self, user_id: UUID, workout_id: int) -> WorkoutReadDTO:
        workout = await self._workout_reader.get(workout_id)

        if workout is None:
            raise WorkoutNotFound(workout_id)

        if workout.public:
            return workout

        if workout.user_id != user_id:
            raise WorkoutAccessDenied()

        return workout
