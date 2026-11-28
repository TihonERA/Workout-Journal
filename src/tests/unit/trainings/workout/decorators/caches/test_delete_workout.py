from uuid import uuid4

import pytest

from src.tests.unit.trainings.factories.workout_factories import WorkoutFactory
from src.tests.unit.trainings.workout.decorators.factories.workout_cache_factories import (
    WorkoutCacheFactory,
)
from src.tests.unit.trainings.workout.decorators.fake_objects.fake_workout_cache import (
    FakeWorkoutCache,
)
from src.trainings.application.decorators.caches.workout.delete_workout import (
    CachedDeleteWorkoutUseCase,
)
from src.trainings.application.ports.workout import IDeleteWorkoutUseCase
from src.trainings.domain.exceptions.workout_exceptions import WorkoutAccessDenied


@pytest.fixture
def cached_use_case(
    delete_workout_use_case: IDeleteWorkoutUseCase, workout_cache: FakeWorkoutCache
) -> CachedDeleteWorkoutUseCase:
    return CachedDeleteWorkoutUseCase(delete_workout_use_case, workout_cache)


async def test_success(
    workout_factory: WorkoutFactory,
    workout_cache_factory: WorkoutCacheFactory,
    cached_use_case: CachedDeleteWorkoutUseCase,
    workout_cache: FakeWorkoutCache,
) -> None:
    workout = await workout_factory.create_workout()
    workout_id = workout.id

    assert workout_id is not None

    await workout_cache_factory.seed_workout(workout)

    await cached_use_case(workout.user_id, workout_id)

    assert await workout_cache.get(workout_id) is None


async def test_access_denied(
    workout_factory: WorkoutFactory,
    workout_cache_factory: WorkoutCacheFactory,
    cached_use_case: CachedDeleteWorkoutUseCase,
    workout_cache: FakeWorkoutCache,
) -> None:
    workout = await workout_factory.create_workout()
    workout_id = workout.id

    assert workout_id is not None

    await workout_cache_factory.seed_workout(workout)

    with pytest.raises(WorkoutAccessDenied):
        await cached_use_case(user_id=uuid4(), workout_id=workout_id)

    assert await workout_cache.get(workout_id) is not None
