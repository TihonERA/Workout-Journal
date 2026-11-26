from src.trainings.application.dto.workout import UpdateWorkoutCommand
from src.trainings.application.ports.workout import (
    IUpdateWorkoutUseCase,
    IWorkoutCacheDeleter,
)
from src.trainings.domain.workout_model import Workout


class CachedUpdateWorkoutUseCase:
    def __init__(
        self, use_case: IUpdateWorkoutUseCase, cache: IWorkoutCacheDeleter
    ) -> None:
        self._use_case = use_case
        self._cache = cache

    async def __call__(self, command: UpdateWorkoutCommand) -> Workout:
        workout = await self._use_case(command)

        await self._cache.delete(command.workout_id)

        return workout
