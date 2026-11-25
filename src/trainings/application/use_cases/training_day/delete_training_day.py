from typing import Protocol
from uuid import UUID

from src.trainings.domain.exceptions.training_day_exceptions import TrainingDayNotFound
from src.trainings.domain.training_day_model import TrainingDay


class TrainingDayDeleter(Protocol):
    async def get(self, id: int) -> TrainingDay | None: ...
    async def delete(self, id: int) -> None: ...


class DeleteTrainingDayUseCase:
    def __init__(
        self,
        tr_day_repo: TrainingDayDeleter,
    ) -> None:
        self._tr_day_repo = tr_day_repo

    async def __call__(self, user_id: UUID, workout_id: int, day_id: int) -> None:
        training_day = await self._tr_day_repo.get(day_id)

        if training_day is None:
            raise TrainingDayNotFound(day_id)

        training_day.ensure_ownership(workout_id)

        await self._tr_day_repo.delete(day_id)
