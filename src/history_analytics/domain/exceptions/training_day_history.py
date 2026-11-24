from src.shared.domain.exceptions import DomainError


class TrainingDayHistoryNotFound(DomainError):
    def __init__(self, day_id: int, id: int) -> None:
        super().__init__(
            f"History with id {id} from day with id: {day_id} was not found"
        )


class TrainingDayHistoryAccessDenied(DomainError):
    def __init__(self) -> None:
        super().__init__("Access to this history was denied")
