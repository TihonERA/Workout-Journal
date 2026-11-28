from src.trainings.application.dto.workout import WorkoutReadDTO
from src.trainings.domain.workout_model import Workout


def assert_same_workouts(
    first_workout: Workout, second_workout: WorkoutReadDTO
) -> None:
    assert first_workout.id == second_workout.id
    assert first_workout.user_id == second_workout.user_id
    assert first_workout.name.value == second_workout.name
    assert first_workout.description == second_workout.description
    assert first_workout.public == second_workout.public
