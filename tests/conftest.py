from typing import Dict
import pytest
from app.schemas.user import User
from app.schemas.word import WordCreate, DialectEnum


@pytest.fixture
def user_one() -> User:
    name = "one"
    return User(
        id=f"user_{name}_id", name=f"user_{name}_name", email=f"user_{name}_email"
    )


@pytest.fixture
def user_two() -> User:
    name = "two"
    return User(
        id=f"user_{name}_id", name=f"user_{name}_name", email=f"user_{name}_email"
    )


@pytest.fixture
def word_create() -> WordCreate:
    return WordCreate(
        title="title",
        explanation="explanation",
        pronunciation="some string",
        usage="usage",
        tags="tags",
        dialect=DialectEnum.hangzhouhua,
    )
