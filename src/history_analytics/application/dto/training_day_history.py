from dataclasses import dataclass
from datetime import datetime

from src.history_analytics.application.dto.exercise_history import (
    ExerciseHistoryDetailDTO,
)


@dataclass(frozen=True)
class CreateTrainingDayHistoryCommand:
    day_id: int
    day_name: str


@dataclass(frozen=True)
class TrainingDayHistoryDetailDTO:
    id: int
    day_id: int
    day_name: str
    created_at: datetime
    exercises_history: list[ExerciseHistoryDetailDTO] | None = None
