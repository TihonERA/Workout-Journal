from typing import Protocol
from uuid import UUID


class TrainingDayAccessValidator(Protocol):
    async def ensure_user_has_training_day(
        self, user_id: UUID, day_id: int
    ) -> None: ...
