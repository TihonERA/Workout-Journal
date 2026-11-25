from uuid import uuid4

import pytest

from src.tests.unit.trainings.conftest import WorkoutFactory
from src.tests.unit.trainings.fake_workout_reader import FakeWorkoutReader
from src.tests.unit.trainings.training_day.fake_training_day_repository import (
    FakeTrainingDayRepository,
)
from src.tests.unit.trainings.training_day.training_day_factories import (
    TrainingDayDTOFactory,
)
from src.trainings.application.use_cases.training_day.create_training_day import (
    CreateTrainingDayUseCase,
)
from src.trainings.domain.exceptions.workout_exceptions import (
    WorkoutNotFound,
)


@pytest.fixture
def use_case(
    workout_reader: FakeWorkoutReader, tr_day_repo: FakeTrainingDayRepository
) -> CreateTrainingDayUseCase:
    return CreateTrainingDayUseCase(
        workout_reader=workout_reader, tr_day_repo=tr_day_repo
    )


async def test_success(
    workout_factory: WorkoutFactory,
    tr_day_dto_factory: TrainingDayDTOFactory,
    use_case: CreateTrainingDayUseCase,
    tr_day_repo: FakeTrainingDayRepository,
) -> None:
    workout = await workout_factory.create_workout()
    workout_id = workout.id

    assert workout_id is not None

    command = tr_day_dto_factory.make_create_tr_day_command(
        user_id=workout.user_id,
        workout_id=workout_id,
    )

    training_day = await use_case(command)

    assert training_day.id is not None

    training_day = await tr_day_repo.get(training_day.id)

    assert training_day is not None

    assert command.workout_id == training_day.workout_id
    assert command.name == training_day.name.value
    assert command.day_order == training_day.day_order.value


async def test_workout_not_found(
    tr_day_dto_factory: TrainingDayDTOFactory, use_case: CreateTrainingDayUseCase
) -> None:
    command = tr_day_dto_factory.make_create_tr_day_command(
        user_id=uuid4(), workout_id=-1
    )

    with pytest.raises(WorkoutNotFound):
        await use_case(command)
