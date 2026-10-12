from uuid import uuid4

from Backend.history_analytics.application.use_cases.create_training_day_history import (
    CreateTrainingDayHistoryUseCase,
)
from Backend.history_analytics.application.dto.training_day_history import (
    CreateTrainingDayHistoryCommand,
)
from unittest.mock import AsyncMock
import pytest

from Backend.tests.unit.history_analytics.training_day_history.fake_training_day_history_repository import (
    FakeTrainingDayHistoryRepository,
)


@pytest.fixture
def use_case(
    fake_tr_day_history_repo: FakeTrainingDayHistoryRepository,
) -> CreateTrainingDayHistoryUseCase:
    return CreateTrainingDayHistoryUseCase(AsyncMock(), fake_tr_day_history_repo)


async def test_create_success(
    use_case: CreateTrainingDayHistoryUseCase,
    fake_tr_day_history_repo: FakeTrainingDayHistoryRepository,
) -> None:
    UNBOUNDED = -1

    command = CreateTrainingDayHistoryCommand(day_id=UNBOUNDED, day_name="name")

    training_day_history = await use_case(uuid4(), command)

    assert training_day_history.id is not None

    fetched_training_day_history = await fake_tr_day_history_repo.get(
        training_day_history.id
    )

    assert fetched_training_day_history is not None
    assert fetched_training_day_history.day_id == command.day_id
    assert fetched_training_day_history.day_name.value == command.day_name
