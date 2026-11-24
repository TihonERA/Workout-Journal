from uuid import uuid4

import pytest

from src.tests.unit.trainings.training_day.helpers import assert_same_tr_days
from src.tests.unit.trainings.training_day.training_day_factories import (
    TrainingDayFactory,
)
from src.tests.unit.trainings.workout_factories import WorkoutFactory
from src.trainings.application.services.training_day_access_service import (
    TrainingDayAccessService,
)
from src.trainings.domain.exceptions.training_day_exceptions import (
    TrainingDayAccessDenied,
    TrainingDayNotFound,
)
from src.trainings.domain.exceptions.workout_exceptions import (
    WorkoutAccessDenied,
    WorkoutNotFound,
)


async def test_success(
    workout_factory: WorkoutFactory,
    tr_day_factory: TrainingDayFactory,
    access_service: TrainingDayAccessService,
) -> None:
    workout = await workout_factory.create_workout()

    assert workout.id is not None

    training_day = await tr_day_factory.create_tr_day(workout_id=workout.id)

    assert training_day.id is not None

    fetched_training_day = await access_service.get_authorized_day(
        user_id=workout.user_id, workout_id=workout.id, day_id=training_day.id
    )

    assert_same_tr_days(training_day, fetched_training_day)


async def test_workout_not_found(
    workout_factory: WorkoutFactory,
    tr_day_factory: TrainingDayFactory,
    access_service: TrainingDayAccessService,
) -> None:
    NOT_BINDED_TO_WORKOUT = 0

    training_day = await tr_day_factory.create_tr_day(workout_id=NOT_BINDED_TO_WORKOUT)

    assert training_day.id is not None

    with pytest.raises(WorkoutNotFound):
        await access_service.get_authorized_day(
            user_id=uuid4(), workout_id=-1, day_id=training_day.id
        )


async def test_workout_access_denied(
    workout_factory: WorkoutFactory,
    tr_day_factory: TrainingDayFactory,
    access_service: TrainingDayAccessService,
) -> None:
    workout = await workout_factory.create_workout()

    assert workout.id is not None

    training_day = await tr_day_factory.create_tr_day(workout_id=workout.id)

    assert training_day.id is not None

    with pytest.raises(WorkoutAccessDenied):
        await access_service.get_authorized_day(
            user_id=uuid4(), workout_id=workout.id, day_id=training_day.id
        )


async def test_tr_day_not_found(
    workout_factory: WorkoutFactory, access_service: TrainingDayAccessService
) -> None:
    workout = await workout_factory.create_workout()

    assert workout.id is not None

    with pytest.raises(TrainingDayNotFound):
        await access_service.get_authorized_day(
            user_id=workout.user_id, workout_id=workout.id, day_id=-1
        )


async def test_tr_day_access_denied(
    workout_factory: WorkoutFactory,
    tr_day_factory: TrainingDayFactory,
    access_service: TrainingDayAccessService,
) -> None:
    workout = await workout_factory.create_workout()

    assert workout.id is not None

    DIFFERENT_WORKOUT = -1

    training_day = await tr_day_factory.create_tr_day(workout_id=DIFFERENT_WORKOUT)

    assert training_day.id is not None

    with pytest.raises(TrainingDayAccessDenied):
        await access_service.get_authorized_day(
            user_id=workout.user_id, workout_id=workout.id, day_id=training_day.id
        )


async def test_ensure_user_has_access_to_training_day_success(
    workout_factory: WorkoutFactory,
    tr_day_factory: TrainingDayFactory,
    access_service: TrainingDayAccessService,
) -> None:
    workout = await workout_factory.create_workout()

    assert workout.id is not None

    training_day = await tr_day_factory.create_tr_day(workout_id=workout.id)

    assert training_day.id is not None

    await access_service.ensure_user_has_training_day(workout.user_id, training_day.id)


async def test_ensure_user_has_access_to_training_day_not_found(
    access_service: TrainingDayAccessService,
) -> None:
    NOT_EXISTING_TRAINING_DAY = -1

    with pytest.raises(TrainingDayNotFound):
        await access_service.ensure_user_has_training_day(
            user_id=uuid4(), day_id=NOT_EXISTING_TRAINING_DAY
        )


async def test_ensure_user_has_access_to_training_day_access_denied(
    workout_factory: WorkoutFactory,
    tr_day_factory: TrainingDayFactory,
    access_service: TrainingDayAccessService,
) -> None:
    workout = await workout_factory.create_workout()

    assert workout.id is not None

    training_day = await tr_day_factory.create_tr_day(workout_id=workout.id)

    assert training_day.id is not None

    with pytest.raises(WorkoutAccessDenied):
        await access_service.ensure_user_has_training_day(
            user_id=uuid4(), day_id=training_day.id
        )
