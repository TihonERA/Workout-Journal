import pytest
from faker import Faker

from src.tests.unit.trainings.training_day.fake_training_day_repository import (
    FakeTrainingDayRepository,
)
from src.tests.unit.trainings.training_day.training_day_factories import (
    TrainingDayDTOFactory,
    TrainingDayFactory,
)


@pytest.fixture
def tr_day_repo() -> FakeTrainingDayRepository:
    return FakeTrainingDayRepository()


@pytest.fixture
def tr_day_factory(
    tr_day_repo: FakeTrainingDayRepository,
    faker: Faker,
) -> TrainingDayFactory:
    return TrainingDayFactory(tr_day_repo, faker)


@pytest.fixture
def tr_day_dto_factory(faker: Faker) -> TrainingDayDTOFactory:
    return TrainingDayDTOFactory(faker)
