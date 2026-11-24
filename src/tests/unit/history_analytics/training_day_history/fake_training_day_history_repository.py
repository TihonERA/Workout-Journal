from copy import copy

from Backend.history_analytics.domain.training_day_history import TrainingDayHistory


class FakeTrainingDayHistoryRepository:
    def __init__(self) -> None:
        self.db: dict[int, TrainingDayHistory] = {}

    async def get(self, id: int) -> TrainingDayHistory | None:
        print(self.db)
        return copy(self.db.get(id))

    async def create(
        self, training_day_history: TrainingDayHistory
    ) -> TrainingDayHistory:
        training_day_history_id = (
            1 if len(self.db) == 0 else list(self.db.keys())[-1] + 1
        )

        training_day_history_copy = copy(training_day_history)
        training_day_history_copy.id = training_day_history_id

        self.db[training_day_history_id] = training_day_history_copy

        print(self.db)
        return copy(training_day_history_copy)
