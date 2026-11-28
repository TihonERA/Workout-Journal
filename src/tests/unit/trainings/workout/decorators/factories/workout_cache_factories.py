from src.tests.unit.trainings.workout.decorators.fake_objects.fake_workout_cache import (
    FakeWorkoutCache,
)
from src.trainings.application.dto.workout import WorkoutReadDTO
from src.trainings.domain.workout_model import Workout


class WorkoutCacheFactory:
    def __init__(self, workout_cache: FakeWorkoutCache) -> None:
        self._cache = workout_cache

    async def seed_workout(self, workout: Workout) -> None:
        UNBOUNDED_WORKOUT_ID = 1

        workout_dto = WorkoutReadDTO(
            id=workout.id or UNBOUNDED_WORKOUT_ID,
            user_id=workout.user_id,
            name=workout.name.value,
            description=workout.description,
            public=workout.public,
            training_days=[],
        )

        await self._cache.set(workout_dto)
