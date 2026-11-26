from typing import Protocol

from src.shared.application.ports import IUnitOfWork
from src.shared.domain.value_objects.entity_title import EntityTitle
from src.trainings.application.dto.workout import CreateWorkoutCommand
from src.trainings.domain.workout_model import Workout


class WorkoutCreator(Protocol):
    async def create(self, workout: Workout) -> Workout: ...


class IUnitOfWorkWorkoutCreator(IUnitOfWork, Protocol):
    @property
    def workout_repo(self) -> WorkoutCreator: ...


class CreateWorkoutUseCase:
    def __init__(self, unit_of_work: IUnitOfWorkWorkoutCreator) -> None:
        self._uow = unit_of_work

    async def __call__(self, command: CreateWorkoutCommand) -> Workout:
        workout = Workout.create(
            user_id=command.user_id,
            name=EntityTitle(command.name),
            description=command.description,
            public=command.public,
        )

        async with self._uow:
            workout = await self._uow.workout_repo.create(workout)

            await self._uow.commit()

            return workout
