import pytest

from src.trainings.domain.exceptions.training_day_exceptions import (
    DayExerciseOrderIntegrityError,
)
from src.trainings.domain.value_objects.exercise_order import ExerciseOrder


def test_under_lowest_border() -> None:
    with pytest.raises((DayExerciseOrderIntegrityError)):
        ExerciseOrder(0)
