from copy import copy

from src.trainings.domain.workout_model import Workout


class FakeWorkoutRepository:
    def __init__(self, storage: dict[int, Workout]) -> None:
        self.storage = storage

    def _get_from_db(self, id: int) -> Workout | None:
        return self.storage.get(id, None)

    async def get(self, id: int) -> Workout | None:
        return copy(self._get_from_db(id))

    async def create(self, workout: Workout) -> Workout:
        if len(self.storage) == 0:
            workout.id = 1
            self.storage[workout.id] = copy(workout)

            return copy(workout)

        last_id = list(self.storage.keys())[-1]
        workout.id = last_id + 1

        self.storage[workout.id] = copy(workout)
        return copy(workout)

    async def save(self, workout: Workout) -> Workout:
        if workout.id is None:
            raise TimeoutError

        workout_db = self._get_from_db(workout.id)

        if workout_db is None:
            raise TimeoutError

        workout_db.name = workout.name
        workout_db.description = workout.description
        workout_db.public = workout.public

        return copy(workout_db)

    async def delete(self, id: int) -> None:
        self.storage.pop(id)
