from pydantic import TypeAdapter

from src.trainings.application.dto.workout import WorkoutReadDTO


class WorkoutCacheSerializer:
    _workout_adapter = TypeAdapter(WorkoutReadDTO)

    @classmethod
    def to_json(cls, workout: WorkoutReadDTO) -> str:
        return cls._workout_adapter.dump_json(workout).decode()

    @classmethod
    def from_json(cls, workout_json: str | bytes) -> WorkoutReadDTO:
        return cls._workout_adapter.validate_json(workout_json)
