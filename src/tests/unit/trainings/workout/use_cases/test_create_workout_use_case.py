import pytest

from src.tests.unit.fake_objects.fake_unit_of_work import FakeUnitOfWork
from src.tests.unit.fake_objects.fake_workout_repository import (
    FakeWorkoutRepository,
)
from src.tests.unit.trainings.factories.workout_factories import (
    WorkoutDTOFactory,
)
from src.trainings.application.use_cases.workout.create_workout import (
    CreateWorkoutUseCase,
)


@pytest.fixture
def use_case(fake_uow: FakeUnitOfWork) -> CreateWorkoutUseCase:
    return CreateWorkoutUseCase(fake_uow)


async def test_create_success(
    use_case: CreateWorkoutUseCase,
    workout_dto_factory: WorkoutDTOFactory,
    workout_repo: FakeWorkoutRepository,
) -> None:
    command = workout_dto_factory.make_create_workout_command()

    workout = await use_case(command)

    assert workout.id is not None

    workout = await workout_repo.get(workout.id)

    assert workout is not None

    assert command.name == workout.name.value
    assert command.description == workout.description
    assert command.public == workout.public
