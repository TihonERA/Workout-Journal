from typing import Protocol

from src.shared.domain.value_objects.entity_title import EntityTitle
from src.trainings.application.dto.training_day import CreateTrainingDayCommand
from src.trainings.application.dto.workout import WorkoutReadDTO
from src.trainings.domain.exceptions.workout_exceptions import WorkoutNotFound
from src.trainings.domain.training_day_model import TrainingDay
from src.trainings.domain.value_objects.day_order import DayOrder


class TrainingDayCreator(Protocol):
    async def create(self, training_day: TrainingDay) -> TrainingDay: ...


class WorkoutReader(Protocol):
    async def get(self, id: int) -> WorkoutReadDTO | None: ...


class CreateTrainingDayUseCase:
    def __init__(
        self,
        workout_reader: WorkoutReader,
        tr_day_repo: TrainingDayCreator,
    ) -> None:
        self._workout_reader = workout_reader
        self._tr_day_repo = tr_day_repo

    async def __call__(self, command: CreateTrainingDayCommand) -> TrainingDay:
        workout = await self._workout_reader.get(command.workout_id)

        if workout is None:
            raise WorkoutNotFound(command.workout_id)

        training_day = TrainingDay.create(
            workout_id=command.workout_id,
            name=EntityTitle(command.name),
            day_order=DayOrder(command.day_order),
        )

        return await self._tr_day_repo.create(training_day)
