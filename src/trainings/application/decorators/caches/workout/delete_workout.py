from uuid import UUID

from src.trainings.application.ports.workout import (
    IDeleteWorkoutUseCase,
    IWorkoutCacheDeleter,
)


class CachedDeleteWorkoutUseCase:
    def __init__(
        self, use_case: IDeleteWorkoutUseCase, cache: IWorkoutCacheDeleter
    ) -> None:
        self._use_case = use_case
        self._cache = cache

    async def __call__(self, user_id: UUID, workout_id: int) -> None:
        await self._use_case(user_id, workout_id)

        await self._cache.delete(workout_id)
