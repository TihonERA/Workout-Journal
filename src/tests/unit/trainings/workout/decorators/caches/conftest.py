import pytest

from src.tests.unit.trainings.workout.decorators.fake_objects.fake_workout_cache import (
    FakeWorkoutCache,
)


@pytest.fixture
def workout_cache() -> FakeWorkoutCache:
    return FakeWorkoutCache()
