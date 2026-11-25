from typing import Final

from redis.asyncio import Redis

from src.trainings.application.dto.workout import WorkoutReadDTO
from src.trainings.infrastructure.caches.serializers.workout_cache_serializer import (
    WorkoutCacheSerializer,
)


class WorkoutCache:
    PREFIX: Final = "workout:"
    TTL: Final = 24 * 3600

    def __init__(self, redis: Redis) -> None:
        self.redis = redis

    def _generate_key(self, workout_id: int) -> str:
        return f"{self.PREFIX}{workout_id}"

    async def get(self, workout_id: int) -> WorkoutReadDTO | None:
        key = self._generate_key(workout_id)

        if workout_json := await self.redis.get(key):
            return WorkoutCacheSerializer.from_json(workout_json)

        return None
