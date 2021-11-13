from flask.testing import FlaskClient
import app.service.word as WordService
import app.service.user as UserService
from app.schemas.word import WordCreate, WordWithFields, WordWithFieldsWithPaging
from app.schemas.user import User


WORD_ID = ""


def test_create_word_from_user_one(
    client_from_user_one: FlaskClient,
    word_create: WordCreate
):
    r = client_from_user_one.post("/private_api/words", json=word_create.dict())
    word_with_fields = WordWithFields(**r.get_json()["response"])
    global WORD_ID
    WORD_ID = word_with_fields.id
    assert r.status_code == 200
    assert word_with_fields.explanation == word_create.explanation


def test_create_same_word_from_user_two(
    client_from_user_two: FlaskClient,
    word_create: WordCreate
):
    r = client_from_user_two.post("/private_api/words", json=word_create.dict())
    assert r.status_code == 409


def test_list_word_from_public(
    client_without_user: FlaskClient,
    word_create: WordCreate
):
    r = client_without_user.get("/private_api/words")
    words_wth_paging = WordWithFieldsWithPaging(
        **r.get_json(["response"])
    )
    assert word_create.explanation in [x.explanation for x in words_wth_paging.data]
    assert r.status_code == 200


def test_delete_word():
    """just to clean up"""
    WordService.delete_word(item_id=WORD_ID)


def test_delete_user(user_one: User, user_two: User):
    """just to clean up"""
    UserService.delete_user(item_id=user_one.id)
    UserService.delete_user(item_id=user_two.id)



