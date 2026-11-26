import pytest
from faker import Faker

from src.tests.unit.trainings.factories.workout_factories import WorkoutDTOFactory


@pytest.fixture
def workout_dto_factory(faker: Faker) -> WorkoutDTOFactory:
    return WorkoutDTOFactory(faker)
