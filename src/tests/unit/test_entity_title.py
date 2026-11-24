import pytest
from faker import Faker

from src.shared.domain.exceptions import TitleError
from src.shared.domain.value_objects.entity_title import EntityTitle


def test_success(faker: Faker) -> None:
    title = faker.name()
    title_object = EntityTitle(title)

    assert title_object.value == title


def test_empty_title() -> None:
    with pytest.raises(TitleError):
        EntityTitle("")


def test_long_title() -> None:
    with pytest.raises(TitleError):
        EntityTitle("long" * 30)
