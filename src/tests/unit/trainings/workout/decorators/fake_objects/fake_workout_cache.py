from typing import Final

from src.trainings.application.dto.workout import WorkoutReadDTO
from src.trainings.infrastructure.caches.serializers.workout_cache_serializer import (
    WorkoutCacheSerializer,
)


class FakeWorkoutCache:
    PREFIX: Final = "workout:"

    def __init__(self) -> None:
        self._cache: dict[str, str] = {}

    def _generate_key(self, id: int) -> str:
        return f"{self.PREFIX}{id}"

    async def get(self, id: int) -> WorkoutReadDTO | None:
        key = self._generate_key(id)

        if workout_json := self._cache.get(key):
            return WorkoutCacheSerializer.from_json(workout_json)

        return None

    async def set(self, workout: WorkoutReadDTO) -> None:
        key = self._generate_key(workout.id)

        self._cache[key] = WorkoutCacheSerializer.to_json(workout)

    async def delete(self, id: int) -> None:
        key = self._generate_key(id)

        self._cache.pop(key)
