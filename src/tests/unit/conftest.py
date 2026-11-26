import pytest

from src.tests.unit.fake_objects.fake_workout_repository import FakeWorkoutRepository


@pytest.fixture
def storage() -> dict:
    return {}


@pytest.fixture
def workout_repo(storage) -> FakeWorkoutRepository:
    return FakeWorkoutRepository(storage)
