from typing import Annotated

from fastapi import APIRouter, Depends, Path

from src.trainings.api.dependencies import get_workout_use_case
from src.trainings.api.schemas.workout import WorkoutResponse
from src.trainings.application.ports.workout import IGetWorkoutUseCase

router = APIRouter(prefix="workouts/")


@router.get("{workout_id}", response_model=WorkoutResponse)
async def get(
    user_id,
    workout_id: Annotated[int, Path()],
    get_workout_use_case: Annotated[IGetWorkoutUseCase, Depends(get_workout_use_case)],
):
    return await get_workout_use_case(user_id, workout_id)
