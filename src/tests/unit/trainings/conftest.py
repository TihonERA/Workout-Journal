import pytest
from faker import Faker

from src.tests.unit.fake_objects.fake_workout_repository import FakeWorkoutRepository
from src.tests.unit.trainings.factories.workout_factories import WorkoutFactory
from src.tests.unit.trainings.fake_objects.fake_workout_reader import (
    FakeWorkoutReader,
)


@pytest.fixture
def workout_reader(storage) -> FakeWorkoutReader:
    return FakeWorkoutReader(storage)


@pytest.fixture
def workout_factory(
    workout_repo: FakeWorkoutRepository, faker: Faker
) -> WorkoutFactory:
    return WorkoutFactory(workout_repo, faker)
