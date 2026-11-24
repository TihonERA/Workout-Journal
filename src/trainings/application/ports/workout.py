from typing import Protocol

from src.trainings.domain.workout_model import Workout


class WorkoutReaderPort(Protocol):
    async def get(self, id: int) -> Workout | None: ...
