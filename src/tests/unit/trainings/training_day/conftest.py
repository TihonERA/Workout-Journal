
import pytest
from faker import Faker

from src.tests.unit.trainings.fake_workout_repository import FakeWorkoutRepository
from src.tests.unit.trainings.training_day.fake_training_day_repository import (
    FakeTrainingDayRepository,
)
from src.tests.unit.trainings.training_day.training_day_factories import (
    TrainingDayDTOFactory,
    TrainingDayFactory,
)
from src.trainings.application.services.training_day_access_service import (
    TrainingDayAccessService,
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


@pytest.fixture
def access_service(
    workout_repo: FakeWorkoutRepository, tr_day_repo: FakeTrainingDayRepository
) -> TrainingDayAccessService:
    return TrainingDayAccessService(workout_repo, tr_day_repo)
