from typing import Self

from src.tests.unit.fake_objects.fake_training_day_repository import (
    FakeTrainingDayRepository,
)
from src.tests.unit.fake_objects.fake_workout_repository import FakeWorkoutRepository


class FakeUnitOfWork:
    def __init__(
        self,
        workout_repo: FakeWorkoutRepository,
        tr_day_repo: FakeTrainingDayRepository,
    ) -> None:
        self.workout_repo = workout_repo
        self.tr_day_repo = tr_day_repo

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        pass

    async def commit(self) -> None:
        pass

    async def rollback(self) -> None:
        pass
