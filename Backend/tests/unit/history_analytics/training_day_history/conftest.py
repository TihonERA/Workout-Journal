import pytest

from Backend.tests.unit.history_analytics.training_day_history.fake_training_day_history_repository import (
    FakeTrainingDayHistoryRepository,
)


@pytest.fixture
def fake_tr_day_history_repo() -> FakeTrainingDayHistoryRepository:
    return FakeTrainingDayHistoryRepository()
