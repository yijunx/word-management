from flask.testing import FlaskClient
from app.schemas.word import DialectEnum


def test_get_dialects(client_without_user: FlaskClient):
    r = client_without_user.get(f"/public_api/words_frontend_utils/dialects")
    assert r.status_code == 200
    assert set(r.get_json()["response"]) == set([x.value for x in DialectEnum])
