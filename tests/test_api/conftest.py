import pytest
from app.app import app
from flask.testing import FlaskClient
from app.schemas.user import User
import jwt


@pytest.fixture
def client_from_user_one(user_one: User) -> FlaskClient:
    token = jwt.encode(payload=user_one.dict(), key="keykeykey")
    with app.test_client() as c:
        c.set_cookie("localhost", "token", token)
        yield c


@pytest.fixture
def client_from_user_two(user_two: User) -> FlaskClient:
    token = jwt.encode(payload=user_two.dict(), key="keykeykey")
    with app.test_client() as c:
        c.set_cookie("localhost", "token", token)
        yield c


@pytest.fixture
def client_without_user() -> FlaskClient:
    with app.test_client() as c:
        yield c

