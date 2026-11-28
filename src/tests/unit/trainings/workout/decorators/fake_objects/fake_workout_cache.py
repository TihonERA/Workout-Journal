from copy import deepcopy
from typing import Final

from src.trainings.application.dto.workout import WorkoutReadDTO


class FakeWorkoutCache:
    PREFIX: Final = "workout:"

    def __init__(self) -> None:
        self._cache: dict[str, WorkoutReadDTO] = {}

    def _generate_key(self, id: int) -> str:
        return f"{self.PREFIX}{id}"

    async def get(self, id: int) -> WorkoutReadDTO | None:
        key = self._generate_key(id)

        return self._cache.get(key)

    async def set(self, workout: WorkoutReadDTO) -> None:
        key = self._generate_key(workout.id)

        self._cache[key] = deepcopy(workout)

    async def delete(self, id: int) -> None:
        key = self._generate_key(id)

        self._cache.pop(key)
