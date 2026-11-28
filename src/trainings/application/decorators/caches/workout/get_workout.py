from typing import Protocol
from uuid import UUID

from src.trainings.application.dto.workout import WorkoutReadDTO
from src.trainings.application.ports.workout import IGetWorkoutUseCase
from src.trainings.domain.exceptions.workout_exceptions import WorkoutAccessDenied


class IWorkoutCache(Protocol):
    async def get(self, id: int) -> WorkoutReadDTO | None: ...
    async def set(self, workout: WorkoutReadDTO) -> None: ...


class CachedGetWorkoutUseCase:
    def __init__(self, use_case: IGetWorkoutUseCase, cache: IWorkoutCache) -> None:
        self._use_case = use_case
        self._cache = cache

    async def __call__(self, user_id: UUID, workout_id: int) -> WorkoutReadDTO:
        workout = await self._cache.get(workout_id)

        if workout is not None:
            if workout.public or workout.user_id == user_id:
                return workout

            raise WorkoutAccessDenied()

        workout = await self._use_case(user_id, workout_id)

        await self._cache.set(workout)

        return workout
