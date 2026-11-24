
import pytest
from faker import Faker

from src.tests.unit.trainings.fake_workout_repository import FakeWorkoutRepository
from src.tests.unit.trainings.workout_factories import WorkoutFactory


@pytest.fixture
def workout_repo() -> FakeWorkoutRepository:
    return FakeWorkoutRepository()


@pytest.fixture
def workout_factory(
    workout_repo: FakeWorkoutRepository, faker: Faker
) -> WorkoutFactory:
    return WorkoutFactory(workout_repo, faker)
