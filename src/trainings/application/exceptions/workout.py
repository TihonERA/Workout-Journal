from src.shared.application.exceptions import ApplicationError


class WorkoutNotCreatedError(ApplicationError):
    def __init__(self) -> None:
        super().__init__("Cant change unexisting workout")


class WorkoutConcurrencyError(ApplicationError):
    def __init__(self, id: int) -> None:
        super().__init__(
            f"Workout with id: {id} was concurrently deleted or does not exist"
        )
