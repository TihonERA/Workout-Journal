import pytest
from faker import Faker

from Backend.tests.unit.history_analytics.training_day_history.training_day_history_factories import (
    TrainingDayHistoryDTOFactory,
)


@pytest.fixture
def tr_day_history_dto_factory(faker: Faker) -> TrainingDayHistoryDTOFactory:
    return TrainingDayHistoryDTOFactory(faker)
