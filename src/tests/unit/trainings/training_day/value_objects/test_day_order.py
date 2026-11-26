import pytest

from src.trainings.domain.exceptions.training_day_exceptions import (
    TrainingDayOrderError,
)
from src.trainings.domain.value_objects.day_order import DayOrder


@pytest.mark.parametrize("order", [0, 8], ids=["Under Lowest", "Above Highest"])
def test_under_borders(order: int) -> None:
    with pytest.raises(TrainingDayOrderError):
        DayOrder(order)
