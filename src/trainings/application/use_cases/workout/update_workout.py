from typing import Protocol

from src.shared.application.ports import IUnitOfWork
from src.shared.domain.value_objects.entity_title import EntityTitle
from src.trainings.application.dto.workout import UpdateWorkoutCommand
from src.trainings.domain.exceptions.workout_exceptions import (
    WorkoutNotFound,
)
from src.trainings.domain.workout_model import Workout


class WorkoutUpdater(Protocol):
    async def get(self, id: int) -> Workout | None: ...

    async def save(self, workout: Workout) -> Workout: ...


class IUnitOfWorkWorkoutUpdater(IUnitOfWork, Protocol):
    @property
    def workout_repo(self) -> WorkoutUpdater: ...


class UpdateWorkoutUseCase:
    def __init__(self, unit_of_work: IUnitOfWorkWorkoutUpdater) -> None:
        self._uow = unit_of_work

    async def __call__(self, command: UpdateWorkoutCommand) -> Workout:
        async with self._uow:
            workout = await self._uow.workout_repo.get(command.workout_id)

            if workout is None:
                raise WorkoutNotFound(command.workout_id)

            workout.ensure_ownership(command.user_id)
            workout.update(
                name=EntityTitle(command.name) if command.name else None,
                description=command.description,
                public=command.public,
            )

            workout = await self._uow.workout_repo.save(workout)

            await self._uow.commit()

            return workout
