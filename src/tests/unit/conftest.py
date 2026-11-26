import pytest

from src.tests.unit.fake_objects.fake_training_day_repository import (
    FakeTrainingDayRepository,
)
from src.tests.unit.fake_objects.fake_unit_of_work import FakeUnitOfWork
from src.tests.unit.fake_objects.fake_workout_repository import FakeWorkoutRepository


@pytest.fixture
def storage() -> dict:
    return {}


@pytest.fixture
def workout_repo(storage) -> FakeWorkoutRepository:
    return FakeWorkoutRepository(storage)


@pytest.fixture
def tr_day_repo() -> FakeTrainingDayRepository:
    return FakeTrainingDayRepository()


@pytest.fixture
def fake_uow(
    workout_repo: FakeWorkoutRepository,
    tr_day_repo: FakeTrainingDayRepository,
) -> FakeUnitOfWork:
    return FakeUnitOfWork(workout_repo=workout_repo, tr_day_repo=tr_day_repo)
