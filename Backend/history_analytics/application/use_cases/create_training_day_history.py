from typing import Protocol
from uuid import UUID

from Backend.history_analytics.application.dto.training_day_history import (
    CreateTrainingDayHistoryCommand,
)
from Backend.history_analytics.domain.training_day_history import TrainingDayHistory
from Backend.shared.domain.value_objects.entity_title import EntityTitle


class TrainingDayHistoryCreater(Protocol):
    async def create(
        self, training_day_history: TrainingDayHistory
    ) -> TrainingDayHistory: ...


class TrainingDayAccessValidator(Protocol):
    async def ensure_user_has_training_day(
        self, user_id: UUID, day_id: int
    ) -> None: ...


class CreateTrainingDayHistoryUseCase:
    def __init__(
        self,
        tr_day_access_validator: TrainingDayAccessValidator,
        tr_day_history_repo: TrainingDayHistoryCreater,
    ) -> None:
        self.tr_day_access_validator = tr_day_access_validator
        self.tr_day_history_repo = tr_day_history_repo

    async def __call__(
        self, user_id: UUID, command: CreateTrainingDayHistoryCommand
    ) -> TrainingDayHistory:
        await self.tr_day_access_validator.ensure_user_has_training_day(
            user_id, command.day_id
        )

        training_day_history = TrainingDayHistory.create(
            day_id=command.day_id, day_name=EntityTitle(command.day_name)
        )

        return await self.tr_day_history_repo.create(training_day_history)
