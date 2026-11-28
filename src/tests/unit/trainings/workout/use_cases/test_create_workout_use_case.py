from src.tests.unit.fake_objects.fake_workout_repository import (
    FakeWorkoutRepository,
)
from src.tests.unit.trainings.factories.workout_factories import (
    WorkoutDTOFactory,
)
from src.trainings.application.use_cases.workout.create_workout import (
    CreateWorkoutUseCase,
)


async def test_create_success(
    create_workout_use_case: CreateWorkoutUseCase,
    workout_dto_factory: WorkoutDTOFactory,
    workout_repo: FakeWorkoutRepository,
) -> None:
    command = workout_dto_factory.make_create_workout_command()

    workout = await create_workout_use_case(command)

    assert workout.id is not None

    workout = await workout_repo.get(workout.id)

    assert workout is not None

    assert command.name == workout.name.value
    assert command.description == workout.description
    assert command.public == workout.public
