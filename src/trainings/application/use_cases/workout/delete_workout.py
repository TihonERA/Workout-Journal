from typing import Protocol
from uuid import UUID

from src.shared.application.ports import IUnitOfWork
from src.trainings.domain.exceptions.workout_exceptions import (
    WorkoutNotFound,
)
from src.trainings.domain.workout_model import Workout


class WorkoutDeleter(Protocol):
    async def get(self, id: int) -> Workout | None: ...

    async def delete(self, id: int) -> None: ...


class IUnitOfWorkWorkoutDeleter(IUnitOfWork, Protocol):
    @property
    def workout_repo(self) -> WorkoutDeleter: ...


class DeleteWorkoutUseCase:
    def __init__(self, unit_of_work: IUnitOfWorkWorkoutDeleter) -> None:
        self._uow = unit_of_work

    async def __call__(self, user_id: UUID, workout_id: int) -> None:
        async with self._uow:
            workout = await self._uow.workout_repo.get(workout_id)

            if workout is None:
                raise WorkoutNotFound(workout_id)

            workout.ensure_ownership(user_id)

            await self._uow.workout_repo.delete(workout_id)

            await self._uow.commit()
