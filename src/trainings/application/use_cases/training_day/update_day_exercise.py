from src.trainings.application.dto.training_day import UpdateDayExerciseCommand
from src.trainings.application.ports.training_day import (
    TrainingDayRepositoryPort,
)
from src.trainings.domain.exceptions.training_day_exceptions import TrainingDayNotFound
from src.trainings.domain.training_day_model import TrainingDay


class UpdateDayExerciseUseCase:
    def __init__(
        self,
        tr_day_repo: TrainingDayRepositoryPort,
    ):
        self._tr_day_repo = tr_day_repo

    async def __call__(self, command: UpdateDayExerciseCommand) -> TrainingDay:
        training_day = await self._tr_day_repo.get(command.day_id)

        if training_day is None:
            raise TrainingDayNotFound(command.day_id)

        training_day.ensure_ownership(command.workout_id)

        training_day.update_exercise(command.exercise_id, command.exercise_order)

        return await self._tr_day_repo.save(training_day)
