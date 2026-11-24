from typing import Protocol
from uuid import UUID

from src.history_analytics.application.ports.training_day_history import (
    TrainingDayAccessValidator,
)
from src.history_analytics.domain.exceptions.training_day_history import (
    TrainingDayHistoryAccessDenied,
    TrainingDayHistoryNotFound,
)
from src.history_analytics.domain.training_day_history import TrainingDayHistory


class TrainingDayHistoryDeleter(Protocol):
    async def get(self, id: int) -> TrainingDayHistory | None: ...
    async def delete(self, id: int) -> None: ...


class DeleteTrainingDayHistoryUseCase:
    def __init__(
        self,
        tr_day_access_validator: TrainingDayAccessValidator,
        tr_day_history_repo: TrainingDayHistoryDeleter,
    ) -> None:
        self.tr_day_access_validator = tr_day_access_validator
        self.tr_day_history_repo = tr_day_history_repo

    async def __call__(self, user_id: UUID, day_id: int, history_id: int) -> None:
        training_day_history = await self.tr_day_history_repo.get(history_id)

        if training_day_history is None:
            raise TrainingDayHistoryNotFound(day_id=day_id, id=history_id)

        if training_day_history.day_id != day_id:
            raise TrainingDayHistoryAccessDenied()

        await self.tr_day_access_validator.ensure_user_has_training_day(user_id, day_id)

        await self.tr_day_history_repo.delete(history_id)
