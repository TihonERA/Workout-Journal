from uuid import UUID

from src.trainings.application.ports.training_day import (
    TrainingDayRepositoryPort,
)
from src.trainings.domain.exceptions.training_day_exceptions import TrainingDayNotFound
from src.trainings.domain.training_day_model import TrainingDay


class DeleteDayExerciseUseCase:
    def __init__(
        self,
        tr_day_repo: TrainingDayRepositoryPort,
    ) -> None:
        self._tr_day_repo = tr_day_repo

    async def __call__(
        self, user_id: UUID, workout_id: int, day_id: int, exercise_id: int
    ) -> TrainingDay:
        training_day = await self._tr_day_repo.get(day_id)

        if training_day is None:
            raise TrainingDayNotFound(day_id)

        training_day.ensure_ownership(workout_id)
        training_day.delete_exercise(exercise_id)

        return await self._tr_day_repo.save(training_day)
