from dataclasses import dataclass

from src.trainings.domain.value_objects.exercise_order import ExerciseOrder


@dataclass
class DayExercise:
    day_id: int | None
    exercise_id: int
    exercise_order: ExerciseOrder
