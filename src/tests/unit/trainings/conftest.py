import pytest
from faker import Faker

from src.tests.unit.fake_objects.fake_training_day_repository import (
    FakeTrainingDayRepository,
)
from src.tests.unit.fake_objects.fake_unit_of_work import FakeUnitOfWork
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


@pytest.fixture
def tr_day_repo() -> FakeTrainingDayRepository:
    return FakeTrainingDayRepository()


@pytest.fixture
def fake_uow(
    workout_repo: FakeWorkoutRepository,
    tr_day_repo: FakeTrainingDayRepository,
) -> FakeUnitOfWork:
    return FakeUnitOfWork(workout_repo=workout_repo, tr_day_repo=tr_day_repo)
