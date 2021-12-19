from flask.testing import FlaskClient
from app.schemas.word import DialectEnum


def test_get_dialects(client_without_user: FlaskClient):
    r = client_without_user.get(f"api/public/words_frontend_utils/dialects")
    assert r.status_code == 200
    assert DialectEnum.hangzhouhua.value in [
        x["name"] for x in r.get_json()["response"]
    ]
