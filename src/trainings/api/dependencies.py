from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.api.dependencies import get_db_session
from src.trainings.application.ports.workout import IGetWorkoutUseCase, IWorkoutReader
from src.trainings.application.use_cases.workout.get_workout import GetWorkoutUseCase
from src.trainings.infrastructure.readers.workout_reader import WorkoutReader


def get_workout_reader(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> IWorkoutReader:
    return WorkoutReader(session)


def get_workout_use_case(
    workout_reader: Annotated[IWorkoutReader, Depends(get_workout_reader)],
) -> IGetWorkoutUseCase:
    return GetWorkoutUseCase(workout_reader)
