from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class CreateTrainingDayCommand:
    workout_id: int
    name: str
    day_order: int


@dataclass(frozen=True)
class UpdateTrainingDayCommand:
    day_id: int
    workout_id: int
    name: str | None = None
    day_order: int | None = None


@dataclass(frozen=True)
class GetTrainingDayCommand:
    user_id: UUID


@dataclass(frozen=True)
class BaseDayExerciseCommand:
    workout_id: int
    day_id: int
    exercise_id: int
    exercise_order: int


@dataclass(frozen=True)
class CreateDayExerciseCommand(BaseDayExerciseCommand): ...


@dataclass(frozen=True)
class UpdateDayExerciseCommand(BaseDayExerciseCommand): ...


@dataclass(frozen=True)
class DayExerciseReadDTO:
    day_id: int
    exercise_id: int
    exercise_order: int


@dataclass(frozen=True)
class TrainingDayReadDTO:
    id: int
    workout_id: int
    name: str
    day_order: int
    day_exercises: list[DayExerciseReadDTO]
