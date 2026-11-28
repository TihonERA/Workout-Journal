from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_serializer

from src.shared.domain.value_objects.entity_title import EntityTitle


class WorkoutResponse(BaseModel):
    id: int
    user_id: UUID
    name: EntityTitle
    description: str | None
    public: bool
    training_days: list

    @field_serializer("name")
    def serialize_name(self, name: EntityTitle) -> str:
        return name.value

    model_config = ConfigDict(from_attributes=True)
