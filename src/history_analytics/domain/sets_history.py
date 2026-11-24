from dataclasses import dataclass
from datetime import datetime


@dataclass
class SetsHistory:
    id: int
    exercise_history_id: int
    set: int | None
    reps: int | None
    weight: float | None
    time_for_set: datetime | None
