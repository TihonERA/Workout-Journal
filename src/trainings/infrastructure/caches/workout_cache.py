from typing import Final

from redis.asyncio import Redis

from src.trainings.application.dto.workout import WorkoutReadDTO
from src.trainings.infrastructure.caches.error_handler import handle_redis_error
from src.trainings.infrastructure.caches.serializers.workout_cache_serializer import (
    WorkoutCacheSerializer,
)


class WorkoutCache:
    PREFIX: Final = "workout:"
    TTL: Final = 24 * 3600

    def __init__(self, redis: Redis) -> None:
        self._redis = redis

    def _generate_key(self, id: int) -> str:
        return f"{self.PREFIX}{id}"

    @handle_redis_error
    async def get(self, id: int) -> WorkoutReadDTO | None:
        key = self._generate_key(id)

        if workout_json := await self._redis.get(key):
            return WorkoutCacheSerializer.from_json(workout_json)

        return None

    @handle_redis_error
    async def set(self, workout: WorkoutReadDTO) -> None:
        key = self._generate_key(workout.id)

        workout_as_json = WorkoutCacheSerializer.to_json(workout)

        await self._redis.set(name=key, value=workout_as_json, ex=self.TTL)

    @handle_redis_error
    async def delete(self, id: int) -> None:
        key = self._generate_key(id)

        await self._redis.delete(key)
