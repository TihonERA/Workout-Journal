from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.cache import redis_client
from src.shared.api.dependencies import get_db_session
from src.trainings.application.decorators.caches.workout.get_workout import (
    CachedGetWorkoutUseCase,
)
from src.trainings.application.ports.workout import (
    IGetWorkoutUseCase,
    IWorkoutCache,
    IWorkoutReader,
)
from src.trainings.application.use_cases.workout.get_workout import GetWorkoutUseCase
from src.trainings.infrastructure.caches.workout_cache import WorkoutCache
from src.trainings.infrastructure.readers.workout_reader import WorkoutReader


def get_workout_reader(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> IWorkoutReader:
    return WorkoutReader(session)


def get_workout_cache() -> IWorkoutCache:
    return WorkoutCache(redis_client)


def get_workout_use_case(
    workout_reader: Annotated[IWorkoutReader, Depends(get_workout_reader)],
    workout_cache: Annotated[IWorkoutCache, Depends(get_workout_cache)],
) -> IGetWorkoutUseCase:
    base_get_workout_use_case = GetWorkoutUseCase(workout_reader)

    return CachedGetWorkoutUseCase(base_get_workout_use_case, workout_cache)
