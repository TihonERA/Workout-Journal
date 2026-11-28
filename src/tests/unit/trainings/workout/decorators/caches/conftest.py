import pytest

from src.tests.unit.trainings.workout.decorators.factories.workout_cache_factories import (
    WorkoutCacheFactory,
)
from src.tests.unit.trainings.workout.decorators.fake_objects.fake_workout_cache import (
    FakeWorkoutCache,
)


@pytest.fixture
def workout_cache() -> FakeWorkoutCache:
    return FakeWorkoutCache()


@pytest.fixture
def workout_cache_factory(workout_cache: FakeWorkoutCache) -> WorkoutCacheFactory:
    return WorkoutCacheFactory(workout_cache)
