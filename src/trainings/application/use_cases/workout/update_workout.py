from typing import Protocol

from src.shared.domain.value_objects.entity_title import EntityTitle
from src.trainings.application.dto.workout import UpdateWorkoutCommand
from src.trainings.domain.exceptions.workout_exceptions import (
    WorkoutNotFound,
)
from src.trainings.domain.workout_model import Workout


class WorkoutUpdater(Protocol):
    async def get(self, id: int) -> Workout | None: ...

    async def save(self, workout: Workout) -> Workout: ...


class UpdateWorkoutUseCase:
    def __init__(self, workout_repo: WorkoutUpdater) -> None:
        self._workout_repo = workout_repo

    async def __call__(self, command: UpdateWorkoutCommand) -> Workout:
        workout = await self._workout_repo.get(command.workout_id)

        if workout is None:
            raise WorkoutNotFound(command.workout_id)

        workout.ensure_ownership(command.user_id)

        workout.update(
            name=EntityTitle(command.name) if command.name else None,
            description=command.description,
            public=command.public,
        )

        workout = await self._workout_repo.save(workout)

        return workout
