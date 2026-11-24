import pytest
from faker import Faker

from Backend.tests.unit.trainings.training_day.training_day_factories import (
    DayExerciseDTOFactory,
)


@pytest.fixture
def day_exercises_dto_factory(faker: Faker) -> DayExerciseDTOFactory:
    return DayExerciseDTOFactory(faker)
