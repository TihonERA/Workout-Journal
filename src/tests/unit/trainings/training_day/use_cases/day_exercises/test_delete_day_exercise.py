import pytest

from src.tests.unit.fake_objects.fake_training_day_repository import (
    FakeTrainingDayRepository,
)
from src.tests.unit.fake_objects.fake_unit_of_work import FakeUnitOfWork
from src.tests.unit.trainings.factories.training_day_factories import (
    TrainingDayFactory,
)
from src.tests.unit.trainings.factories.workout_factories import (
    WorkoutFactory,
)
from src.tests.unit.trainings.training_day.helpers import (
    assert_same_tr_days,
    get_exercise_id_order,
)
from src.trainings.application.use_cases.training_day.delete_day_exercise import (
    DeleteDayExerciseUseCase,
)
from src.trainings.domain.exceptions.training_day_exceptions import (
    TrainingDayAccessDenied,
)


@pytest.fixture
def use_case(fake_uow: FakeUnitOfWork) -> DeleteDayExerciseUseCase:
    return DeleteDayExerciseUseCase(fake_uow)


async def test_success(
    workout_factory: WorkoutFactory,
    tr_day_factory: TrainingDayFactory,
    use_case: DeleteDayExerciseUseCase,
    tr_day_repo: FakeTrainingDayRepository,
) -> None:
    workout = await workout_factory.create_workout()

    assert workout.id is not None

    training_day = await tr_day_factory.create_tr_day(workout_id=workout.id)
    await tr_day_factory.create_day_exercises_in_training_day(training_day)

    assert training_day.id is not None
    assert get_exercise_id_order(training_day) == [1, 2, 3]

    await use_case(
        user_id=workout.user_id,
        workout_id=workout.id,
        day_id=training_day.id,
        exercise_id=3,
    )

    training_day_after_update = await tr_day_repo.get(training_day.id)

    assert training_day_after_update is not None

    assert_same_tr_days(training_day, training_day_after_update)
    assert get_exercise_id_order(training_day_after_update) == [1, 2]


async def test_atomicity(
    workout_factory: WorkoutFactory,
    tr_day_factory: TrainingDayFactory,
    use_case: DeleteDayExerciseUseCase,
    tr_day_repo: FakeTrainingDayRepository,
) -> None:
    workout = await workout_factory.create_workout()
    different_workout = await workout_factory.create_workout()

    assert workout.id is not None
    assert different_workout.id is not None

    training_day = await tr_day_factory.create_tr_day(workout_id=workout.id)
    await tr_day_factory.create_day_exercises_in_training_day(training_day)

    assert training_day.id is not None
    assert get_exercise_id_order(training_day) == [1, 2, 3]

    with pytest.raises(TrainingDayAccessDenied):
        await use_case(
            user_id=different_workout.user_id,
            workout_id=different_workout.id,
            day_id=training_day.id,
            exercise_id=3,
        )

    training_day_after_update = await tr_day_repo.get(training_day.id)

    assert training_day_after_update is not None

    assert_same_tr_days(training_day, training_day_after_update)
    assert get_exercise_id_order(training_day_after_update) == [1, 2, 3]
