from faker import Faker

from Backend.history_analytics.application.dto.training_day_history import (
    CreateTrainingDayHistoryCommand,
)


class TrainingDayHistoryDTOFactory:
    def __init__(self, faker: Faker) -> None:
        self.faker = faker

    def make_training_day_history_create_command(
        self, day_id: int, day_name: str | None = None
    ) -> CreateTrainingDayHistoryCommand:
        return CreateTrainingDayHistoryCommand(
            day_id=day_id,
            day_name=day_name if day_name is not None else self.faker.name(),
        )
