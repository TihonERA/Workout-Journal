from uuid import uuid4

import pytest

from src.tests.unit.trainings.factories.workout_factories import WorkoutFactory
from src.tests.unit.trainings.workout.helpers import assert_same_workouts
from src.trainings.application.use_cases.workout.get_workout import (
    GetWorkoutUseCase,
)
from src.trainings.domain.exceptions.workout_exceptions import (
    WorkoutAccessDenied,
    WorkoutNotFound,
)


async def test_success(
    workout_factory: WorkoutFactory, get_workout_use_case: GetWorkoutUseCase
) -> None:
    workout = await workout_factory.create_workout()
    workout_id = workout.id

    assert workout_id is not None

    fetched_workout = await get_workout_use_case(workout.user_id, workout_id)

    assert fetched_workout is not None

    assert_same_workouts(workout, fetched_workout)


async def test_not_found(get_workout_use_case: GetWorkoutUseCase) -> None:
    UNKNOWN_WORKOUT_ID = -1

    with pytest.raises(WorkoutNotFound):
        await get_workout_use_case(user_id=uuid4(), workout_id=UNKNOWN_WORKOUT_ID)


async def test_read_public(
    workout_factory: WorkoutFactory, get_workout_use_case: GetWorkoutUseCase
) -> None:
    workout = await workout_factory.create_workout(public=True)
    workout_id = workout.id

    assert workout_id is not None

    fetched_workout = await get_workout_use_case(user_id=uuid4(), workout_id=workout_id)

    assert fetched_workout is not None

    assert_same_workouts(workout, fetched_workout)


async def test_access_denied(
    workout_factory: WorkoutFactory, get_workout_use_case: GetWorkoutUseCase
) -> None:
    workout = await workout_factory.create_workout()
    workout_id = workout.id

    assert workout_id is not None

    with pytest.raises(WorkoutAccessDenied):
        await get_workout_use_case(user_id=uuid4(), workout_id=workout_id)
