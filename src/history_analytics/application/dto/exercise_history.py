from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class SetsHistoryReadDTO:
    id: int
    set: int | None
    reps: int | None
    weight: float | None
    time_for_set: datetime | None


@dataclass(frozen=True)
class ExerciseHistoryDetailDTO:
    id: int
    user_id: UUID
    exercise_id: int
    training_day_history_id: int | None
    created_at: datetime
    sets_history: list[SetsHistoryReadDTO] | None = None
