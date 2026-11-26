from src.trainings.application.dto.training_day import CreateDayExerciseCommand
from src.trainings.application.ports.training_day import (
    IUnitOfWorkTrainingDay,
)
from src.trainings.domain.exceptions.training_day_exceptions import TrainingDayNotFound
from src.trainings.domain.training_day_model import TrainingDay


class CreateDayExerciseUseCase:
    def __init__(self, unit_of_work: IUnitOfWorkTrainingDay) -> None:
        self._uow = unit_of_work

    async def __call__(self, command: CreateDayExerciseCommand) -> TrainingDay:
        async with self._uow:
            training_day = await self._uow.tr_day_repo.get(command.day_id)

            if training_day is None:
                raise TrainingDayNotFound(command.day_id)

            training_day.ensure_ownership(command.workout_id)
            training_day.add_exercise(command.exercise_id, command.exercise_order)

            training_day = await self._uow.tr_day_repo.save(training_day)

            await self._uow.commit()

            return training_day
