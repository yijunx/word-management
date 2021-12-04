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
        title="untitled",
        explanation="explanation",
        pronunciation="some string",
        usage="usage",
        tags=["xx", "yy", "zz"],
        dialect=DialectEnum.hangzhouhua,
    )


@pytest.fixture
def word_create_to_merge() -> WordCreate:
    return WordCreate(
        title="title_to_merge",
        explanation="explanation2",
        pronunciation="some string2",
        usage="usage2",
        tags=["tags2"],
        dialect=DialectEnum.hangzhouhua,
    )
