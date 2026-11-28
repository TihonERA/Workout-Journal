from uuid import uuid4

import pytest

from src.tests.unit.trainings.factories.workout_factories import (
    WorkoutDTOFactory,
    WorkoutFactory,
)
from src.tests.unit.trainings.workout.decorators.factories.workout_cache_factories import (
    WorkoutCacheFactory,
)
from src.tests.unit.trainings.workout.decorators.fake_objects.fake_workout_cache import (
    FakeWorkoutCache,
)
from src.trainings.application.decorators.caches.workout.update_workout import (
    CachedUpdateWorkoutUseCase,
)
from src.trainings.application.ports.workout import IUpdateWorkoutUseCase
from src.trainings.domain.exceptions.workout_exceptions import WorkoutAccessDenied


@pytest.fixture
def cached_use_case(
    update_workout_use_case: IUpdateWorkoutUseCase,
    workout_cache: FakeWorkoutCache,
    workout_dto_factory: WorkoutDTOFactory,
) -> CachedUpdateWorkoutUseCase:
    return CachedUpdateWorkoutUseCase(update_workout_use_case, workout_cache)


async def test_success(
    workout_factory: WorkoutFactory,
    workout_cache_factory: WorkoutCacheFactory,
    workout_dto_factory: WorkoutDTOFactory,
    cached_use_case: CachedUpdateWorkoutUseCase,
    workout_cache: FakeWorkoutCache,
) -> None:
    workout = await workout_factory.create_workout()
    workout_id = workout.id

    assert workout_id is not None

    await workout_cache_factory.seed_workout(workout)

    command = workout_dto_factory.make_update_workout_command(
        user_id=workout.user_id,
        workout_id=workout_id,
        name="new_name",
        description="new_desc",
        public=True,
    )

    await cached_use_case(command)

    workout_from_cache = await workout_cache.get(workout_id)

    assert workout_from_cache is None


async def test_access_denied(
    workout_factory: WorkoutFactory,
    workout_cache_factory: WorkoutCacheFactory,
    workout_dto_factory: WorkoutDTOFactory,
    cached_use_case: CachedUpdateWorkoutUseCase,
    workout_cache: FakeWorkoutCache,
) -> None:
    workout = await workout_factory.create_workout()
    workout_id = workout.id

    assert workout_id is not None

    await workout_cache_factory.seed_workout(workout)

    command = workout_dto_factory.make_update_workout_command(
        user_id=uuid4(), workout_id=workout_id
    )

    with pytest.raises(WorkoutAccessDenied):
        await cached_use_case(command)

    workout_from_cache = await workout_cache.get(workout_id)

    assert workout_from_cache is not None
