from src.trainings.application.dto.workout import WorkoutReadDTO
from src.trainings.domain.workout_model import Workout


class FakeWorkoutReader:
    def __init__(self, storage: dict[int, Workout]) -> None:
        self.storage = storage

    async def get(self, id: int) -> WorkoutReadDTO | None:
        workout = self.storage.get(id)

        if workout is None:
            return None

        WORKOUT_ID_IF_NOT_ALREADY_EXIST = 1

        return WorkoutReadDTO(
            id=(
                workout.id
                if workout.id is not None
                else WORKOUT_ID_IF_NOT_ALREADY_EXIST
            ),
            user_id=workout.user_id,
            name=workout.name.value,
            description=workout.description,
            public=workout.public,
            training_days=[],
        )
