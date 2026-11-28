from uuid import uuid4

import pytest

from src.tests.unit.trainings.factories.workout_factories import WorkoutFactory
from src.tests.unit.trainings.workout.decorators.factories.workout_cache_factories import (
    WorkoutCacheFactory,
)
from src.tests.unit.trainings.workout.decorators.fake_objects.fake_workout_cache import (
    FakeWorkoutCache,
)
from src.tests.unit.trainings.workout.helpers import assert_same_workouts
from src.trainings.application.decorators.caches.workout.get_workout import (
    CachedGetWorkoutUseCase,
)
from src.trainings.application.use_cases.workout.get_workout import GetWorkoutUseCase
from src.trainings.domain.exceptions.workout_exceptions import (
    WorkoutAccessDenied,
    WorkoutNotFound,
)


@pytest.fixture
def cached_use_case(
    get_workout_use_case: GetWorkoutUseCase, workout_cache: FakeWorkoutCache
) -> CachedGetWorkoutUseCase:
    return CachedGetWorkoutUseCase(get_workout_use_case, workout_cache)


async def test_success(
    workout_factory: WorkoutFactory,
    cached_use_case: CachedGetWorkoutUseCase,
    workout_cache: FakeWorkoutCache,
) -> None:
    workout = await workout_factory.create_workout()
    workout_id = workout.id

    assert workout_id is not None

    await cached_use_case(workout.user_id, workout_id)

    workout_from_cache = await workout_cache.get(workout_id)

    assert workout_from_cache is not None
    assert_same_workouts(workout, workout_from_cache)


async def test_access_denied_cache_miss(
    workout_factory: WorkoutFactory,
    cached_use_case: CachedGetWorkoutUseCase,
    workout_cache: FakeWorkoutCache,
) -> None:
    workout = await workout_factory.create_workout()
    workout_id = workout.id

    assert workout_id is not None

    with pytest.raises(WorkoutAccessDenied):
        await cached_use_case(uuid4(), workout_id)

    workout_from_cache = await workout_cache.get(workout_id)

    assert workout_from_cache is None


async def test_access_denied_cache_hit(
    workout_factory: WorkoutFactory,
    workout_cache_factory: WorkoutCacheFactory,
    cached_use_case: CachedGetWorkoutUseCase,
    workout_cache: FakeWorkoutCache,
) -> None:
    workout = await workout_factory.create_workout()
    workout_id = workout.id

    assert workout_id is not None

    await workout_cache_factory.seed_workout(workout)

    with pytest.raises(WorkoutAccessDenied):
        await cached_use_case(uuid4(), workout_id)
