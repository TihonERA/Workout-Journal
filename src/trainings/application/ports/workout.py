from typing import Protocol
from uuid import UUID

from src.trainings.application.dto.workout import (
    CreateWorkoutCommand,
    UpdateWorkoutCommand,
    WorkoutReadDTO,
)
from src.trainings.domain.workout_model import Workout


class IWorkoutReader(Protocol):
    async def get(self, id: int) -> WorkoutReadDTO | None: ...


class ICreateWorkoutUseCase(Protocol):
    async def __call__(self, command: CreateWorkoutCommand) -> Workout: ...


class IDeleteWorkoutUseCase(Protocol):
    async def __call__(self, user_id: UUID, workout_id: int) -> None: ...


class IGetWorkoutUseCase(Protocol):
    async def __call__(self, user_id: UUID, workout_id: int) -> WorkoutReadDTO: ...


class IUpdateWorkoutUseCase(Protocol):
    async def __call__(self, command: UpdateWorkoutCommand) -> Workout: ...


class IWorkoutCacheDeleter(Protocol):
    async def delete(self, id: int) -> None: ...


class IWorkoutCache(Protocol):
    async def get(self, id: int) -> WorkoutReadDTO | None: ...
    async def set(self, workout: WorkoutReadDTO) -> None: ...
    async def delete(self, id: int) -> None: ...
