from src.shared.domain.value_objects.entity_title import EntityTitle
from src.trainings.application.dto.training_day import UpdateTrainingDayCommand
from src.trainings.application.ports.training_day import IUnitOfWorkTrainingDay
from src.trainings.domain.exceptions.training_day_exceptions import TrainingDayNotFound
from src.trainings.domain.training_day_model import TrainingDay
from src.trainings.domain.value_objects.day_order import DayOrder


class UpdateTrainingDay:
    def __init__(self, unit_of_work: IUnitOfWorkTrainingDay) -> None:
        self._uow = unit_of_work

    async def __call__(self, command: UpdateTrainingDayCommand) -> TrainingDay:
        async with self._uow:
            training_day = await self._uow.tr_day_repo.get(command.day_id)

            if training_day is None:
                raise TrainingDayNotFound(command.day_id)

            training_day.ensure_ownership(command.workout_id)
            training_day.update(
                EntityTitle(command.name) if command.name else None,
                DayOrder(command.day_order) if command.day_order else None,
            )

            training_day = await self._uow.tr_day_repo.save(training_day)

            await self._uow.commit()

            return training_day
