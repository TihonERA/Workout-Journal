import pytest
from faker import Faker

from src.tests.unit.trainings.fake_workout_reader import FakeWorkoutReader
from src.tests.unit.trainings.fake_workout_repository import FakeWorkoutRepository
from src.tests.unit.trainings.workout_factories import WorkoutFactory


@pytest.fixture
def storage() -> dict:
    return {}


@pytest.fixture
def workout_repo(storage) -> FakeWorkoutRepository:
    return FakeWorkoutRepository(storage)


@pytest.fixture
def workout_reader(storage) -> FakeWorkoutReader:
    return FakeWorkoutReader(storage)


@pytest.fixture
def workout_factory(
    workout_repo: FakeWorkoutRepository, faker: Faker
) -> WorkoutFactory:
    return WorkoutFactory(workout_repo, faker)
