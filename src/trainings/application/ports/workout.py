from typing import Protocol

from src.trainings.application.dto.workout import WorkoutReadDTO


class IWorkoutReader(Protocol):
    async def get(self, id: int) -> WorkoutReadDTO | None: ...
