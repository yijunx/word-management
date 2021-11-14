from flask.testing import FlaskClient
from app.schemas.field_version import (
    FieldEnum,
    FieldVersion,
    FieldVersionCreate,
    FieldVersionWithPaging,
)
import app.service.word as WordService
import app.service.user as UserService
from app.schemas.word import WordCreate, WordWithFields, WordWithFieldsWithPaging, Word
from app.schemas.user import User


WORD_ID = ""
FIELD_VERSION_ID = ""
NEW_FIELD_VERSION_CONTENT = "new content"


def test_create_word_from_user_one(
    client_from_user_one: FlaskClient, word_create: WordCreate
):
    r = client_from_user_one.post("/private_api/words", json=word_create.dict())
    word_with_fields = WordWithFields(**r.get_json()["response"])
    global WORD_ID
    WORD_ID = word_with_fields.id
    assert r.status_code == 200
    assert word_with_fields.explanation == word_create.explanation
    assert word_with_fields.tags == word_create.tags
    assert word_with_fields.usage == word_create.usage


def test_create_same_word_from_user_two(
    client_from_user_two: FlaskClient, word_create: WordCreate
):
    r = client_from_user_two.post("/private_api/words", json=word_create.dict())
    assert r.status_code == 409


def test_list_word_from_public(
    client_without_user: FlaskClient, word_create: WordCreate
):
    r = client_without_user.get("/public_api/words")
    print(r.get_json())
    words_wth_paging = WordWithFieldsWithPaging(**r.get_json()["response"])
    assert word_create.explanation in [x.explanation for x in words_wth_paging.data]
    assert word_create.usage in [x.usage for x in words_wth_paging.data]
    assert word_create.pronunciation in [x.pronunciation for x in words_wth_paging.data]
    assert word_create.tags in [x.tags for x in words_wth_paging.data]
    assert r.status_code == 200


def test_patch_word_from_user_two(client_from_user_two: FlaskClient):
    r = client_from_user_two.patch(
        f"/private_api/words/{WORD_ID}", json={"title": "new_title"}
    )
    assert r.status_code == 403


def test_list_my_word_from_user_two(client_from_user_two: FlaskClient):
    r = client_from_user_two.get(f"/private_api/words")
    assert r.status_code == 200
    words_wth_paging = WordWithFieldsWithPaging(**r.get_json()["response"])
    assert len(words_wth_paging.data) == 0


def test_patch_word_from_user_one(client_from_user_one: FlaskClient):
    r = client_from_user_one.patch(
        f"/private_api/words/{WORD_ID}", json={"title": "new_title"}
    )
    word = Word(**r.get_json()["response"])
    assert r.status_code == 200
    assert word.title == "new_title"


def test_add_field_version_from_user_two(client_from_user_two: FlaskClient):
    r = client_from_user_two.post(
        f"/private_api/field_versions",
        json=FieldVersionCreate(
            word_id=WORD_ID,
            field=FieldEnum.explanation,
            content=NEW_FIELD_VERSION_CONTENT,
        ).dict(),
    )
    field_version = FieldVersion(**r.get_json()["response"])
    global FIELD_VERSION_ID
    FIELD_VERSION_ID = field_version.id
    assert r.status_code == 200


def test_list_field_version_from_public(client_without_user: FlaskClient):
    r = client_without_user.get(
        f"/public_api/field_versions", query_string={"word_id": WORD_ID}
    )
    field_versions_with_paging = FieldVersionWithPaging(**r.get_json()["response"])
    assert r.status_code == 200
    assert NEW_FIELD_VERSION_CONTENT in [
        x.content for x in field_versions_with_paging.data
    ]


def test_patch_field_version(client_from_user_two: FlaskClient):
    r = client_from_user_two.patch(
        f"/private_api/field_versions/{FIELD_VERSION_ID}",
        json={"content": "new content"},
    )
    assert r.status_code == 200


def test_patch_field_version_from_user_one(client_from_user_one: FlaskClient):
    r = client_from_user_one.patch(
        f"/private_api/field_versions/{FIELD_VERSION_ID}",
        json={"content": "new content"},
    )
    assert r.status_code == 403


def test_delete_word():
    """just to clean up"""
    WordService.delete_word(item_id=WORD_ID)


def test_delete_user(user_one: User, user_two: User):
    """just to clean up"""
    UserService.delete_user(item_id=user_one.id)
    UserService.delete_user(item_id=user_two.id)
