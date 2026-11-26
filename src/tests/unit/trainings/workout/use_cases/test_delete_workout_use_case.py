from uuid import uuid4

import pytest

from src.tests.unit.fake_objects.fake_workout_repository import (
    FakeWorkoutRepository,
)
from src.tests.unit.trainings.factories.workout_factories import WorkoutFactory
from src.trainings.application.use_cases.workout.delete_workout import (
    DeleteWorkoutUseCase,
)
from src.trainings.domain.exceptions.workout_exceptions import (
    WorkoutAccessDenied,
    WorkoutNotFound,
)


@pytest.fixture
def use_case(workout_repo: FakeWorkoutRepository) -> DeleteWorkoutUseCase:
    return DeleteWorkoutUseCase(workout_repo)


async def test_success(
    workout_factory: WorkoutFactory,
    use_case: DeleteWorkoutUseCase,
    workout_repo: FakeWorkoutRepository,
) -> None:
    workout = await workout_factory.create_workout()
    workout_id = workout.id

    assert workout_id is not None

    await use_case(workout.user_id, workout_id)

    assert await workout_repo.get(workout_id) is None


async def test_not_found(use_case: DeleteWorkoutUseCase) -> None:
    with pytest.raises(WorkoutNotFound):
        await use_case(user_id=uuid4(), workout_id=-1)


async def test_access_denied(
    workout_factory: WorkoutFactory,
    use_case: DeleteWorkoutUseCase,
    workout_repo: FakeWorkoutRepository,
) -> None:
    workout = await workout_factory.create_workout()
    workout_id = workout.id

    assert workout_id is not None

    with pytest.raises(WorkoutAccessDenied):
        await use_case(user_id=uuid4(), workout_id=workout_id)

    assert await workout_repo.get(workout_id) is not None
