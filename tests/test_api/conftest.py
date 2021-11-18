import pytest
from app.app import app
from flask.testing import FlaskClient
from app.schemas.user import User
import jwt
import os


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
def client_from_admin() -> FlaskClient:
    admin_user = User(
        id=os.getenv("ADMIN_USER_ID"),
        name=os.getenv("ADMIN_USER_NAME"),
        email=os.getenv("ADMIN_USER_EMAIL"),
    )
    token = jwt.encode(payload=admin_user.dict(), key="keykeykey")
    with app.test_client() as c:
        c.set_cookie("localhost", "token", token)
        yield c


@pytest.fixture
def client_without_user() -> FlaskClient:
    with app.test_client() as c:
        yield c


@pytest.fixture
def admin_user_to_add() -> User:
    return User(id="admin_user_test", name="admin_user_name", email="admin_user_email")
