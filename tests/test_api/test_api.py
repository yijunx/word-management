from flask.testing import FlaskClient
from app.schemas.field_version import (
    FieldEnum,
    FieldVersion,
    FieldVersionCreate,
    FieldVersionWithPaging,
)
from app.schemas.word import (
    WordContribution,
    WordCreate,
    WordWithFields,
    WordWithFieldsWithPaging,
    Word,
)
from app.schemas.user import User
from app.schemas.suggestion import Suggestion, SuggestionWithPaging
import app.service.word as WordService
import app.service.user as UserService


WORD_ID = ""
WORD_ID_TO_MERGE = ""
FIELD_VERSION_ID = ""
SUGGESTION_ID = ""
NEW_FIELD_VERSION_CONTENT = "new content"
WORD_NEW_TITLE = "new_title"


def test_create_word_from_user_one(
    client_from_user_one: FlaskClient, word_create: WordCreate
):
    r = client_from_user_one.post("/private_api/words", json=word_create.dict())
    word_with_fields = WordWithFields(**r.get_json()["response"])
    global WORD_ID
    WORD_ID = word_with_fields.id
    assert r.status_code == 200
    assert word_with_fields.explanation == word_create.explanation
    assert set(word_with_fields.tags) == set(word_create.tags)
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
    assert r.status_code == 200


def test_patch_word_from_user_two(client_from_user_two: FlaskClient):
    r = client_from_user_two.patch(
        f"/private_api/words/{WORD_ID}", json={"title": WORD_NEW_TITLE}
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


def test_list_my_versions_from_user_two(client_from_user_two: FlaskClient):
    r = client_from_user_two.get(
        f"/private_api/field_versions", query_string={"word_id": WORD_ID}
    )
    field_versions_with_paging = FieldVersionWithPaging(**r.get_json()["response"])
    assert r.status_code == 200
    assert NEW_FIELD_VERSION_CONTENT in [
        x.content for x in field_versions_with_paging.data
    ]
    assert len(field_versions_with_paging.data) == 1


def test_list_field_version_from_public(client_without_user: FlaskClient):
    r = client_without_user.get(
        f"/public_api/field_versions",
        query_string={"word_id": WORD_ID, "field": "explanation"},
    )
    field_versions_with_paging = FieldVersionWithPaging(**r.get_json()["response"])
    assert r.status_code == 200
    assert NEW_FIELD_VERSION_CONTENT in [
        x.content for x in field_versions_with_paging.data
    ]
    assert len(field_versions_with_paging.data) == 2


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


def test_add_suggestion_from_user_one(client_from_user_one: FlaskClient):
    r = client_from_user_one.post(
        f"/private_api/suggestions",
        json={
            "content": "suggestion",
            "word_id": WORD_ID,
            "version_id": FIELD_VERSION_ID,
        },
    )
    sugguestion = Suggestion(**r.get_json()["response"])
    global SUGGESTION_ID
    SUGGESTION_ID = sugguestion.id
    assert r.status_code == 200
    assert sugguestion.content == "suggestion"


def test_patch_suggestion_from_user_two(client_from_user_two: FlaskClient):
    r = client_from_user_two.patch(
        f"/private_api/suggestions/{SUGGESTION_ID}",
        json={"content": "new content"},
    )
    assert r.status_code == 403


def test_approve_suggestion_from_user_two(client_from_user_two: FlaskClient):
    r = client_from_user_two.post(
        f"/private_api/field_versions/{FIELD_VERSION_ID}/accept_suggestion",
        json={"suggestion_id": SUGGESTION_ID},
    )
    assert r.status_code == 200


def test_list_suggestion_from_public(client_without_user: FlaskClient):
    r = client_without_user.get(
        f"/public_api/suggestions",
        query_string={"word_id": WORD_ID, "version_id": FIELD_VERSION_ID},
    )
    suggestion_with_paging = SuggestionWithPaging(**r.get_json()["response"])
    assert r.status_code == 200
    assert len(suggestion_with_paging.data) == 1
    assert suggestion_with_paging.data[0].accepted == True


def test_get_a_word_from_public(
    client_without_user: FlaskClient, word_create: WordCreate
):
    r = client_without_user.get(f"/public_api/words/{WORD_ID}")
    word = WordWithFields(**r.get_json()["response"])
    assert r.status_code == 200
    assert set(word.tags) == set(word_create.tags)


def test_list_word_contributors(client_without_user: FlaskClient):
    r = client_without_user.get(f"/public_api/words/{WORD_ID}/contributors")
    word_contribution = WordContribution(**r.get_json()["response"])
    assert r.status_code == 200
    assert len(word_contribution.data) == 2


def test_vote_a_field_version(
    client_from_user_two: FlaskClient,
):
    r = client_from_user_two.post(
        f"/private_api/field_versions/{FIELD_VERSION_ID}/vote", json={"vote_up": True}
    )
    assert r.status_code == 200


def test_vote_a_field_version_again(
    client_from_user_two: FlaskClient,
):
    r = client_from_user_two.post(
        f"/private_api/field_versions/{FIELD_VERSION_ID}/vote", json={"vote_up": True}
    )
    assert r.status_code == 409


def test_unvote_a_field_version(
    client_from_user_two: FlaskClient,
):
    r = client_from_user_two.post(
        f"/private_api/field_versions/{FIELD_VERSION_ID}/unvote"
    )
    assert r.status_code == 200


def test_unvote_a_not_voted_field_version(
    client_from_user_one: FlaskClient,
):
    r = client_from_user_one.post(
        f"/private_api/field_versions/{FIELD_VERSION_ID}/unvote"
    )
    assert r.status_code == 404


def test_create_word_from_user_two(
    client_from_user_two: FlaskClient, word_create_to_merge: WordCreate
):
    """later we will merge"""
    r = client_from_user_two.post(
        "/private_api/words", json=word_create_to_merge.dict()
    )
    word_with_fields = WordWithFields(**r.get_json()["response"])
    global WORD_ID_TO_MERGE
    WORD_ID_TO_MERGE = word_with_fields.id
    assert r.status_code == 200
    assert word_with_fields.explanation == word_create_to_merge.explanation
    assert set(word_with_fields.tags) == set(word_create_to_merge.tags)
    assert word_with_fields.usage == word_create_to_merge.usage


def test_merge_word(client_from_admin: FlaskClient):
    r = client_from_admin.post(
        f"/private_api/words/{WORD_ID_TO_MERGE}/merge_into_another",
        json={"word_id_to_merge_into": WORD_ID},
    )
    assert r.status_code == 200


def test_get_field_versions_from_merged(
    client_without_user: FlaskClient,
    word_create_to_merge: WordCreate,
    word_create: WordCreate,
):
    r = client_without_user.get(
        f"/public_api/field_versions",
        query_string={"word_id": WORD_ID, "field": "explanation"},
    )
    field_versions_with_paging = FieldVersionWithPaging(**r.get_json()["response"])
    assert r.status_code == 200
    assert word_create_to_merge.explanation in [
        x.content for x in field_versions_with_paging.data
    ]
    assert word_create.explanation in [
        x.content for x in field_versions_with_paging.data
    ]


def test_merge_with_user_account(client_from_user_two: FlaskClient):
    r = client_from_user_two.post(
        f"/private_api/words/{WORD_ID_TO_MERGE}/merge_into_another",
        json={"word_id_to_merge_into": WORD_ID},
    )
    assert r.status_code == 403


def test_lock_word(client_from_admin: FlaskClient):
    r = client_from_admin.post(
        f"/private_api/words/{WORD_ID}/lock",
    )
    assert r.status_code == 200


def test_unlock_merged_word(client_from_admin: FlaskClient):
    r = client_from_admin.post(
        f"/private_api/words/{WORD_ID_TO_MERGE}/lock",
    )
    assert r.status_code == 500


def test_deactivate_word(client_from_admin: FlaskClient):
    r = client_from_admin.post(
        f"/private_api/words/{WORD_ID}/deactivate",
    )
    assert r.status_code == 200


def test_list_word_from_public_after_deactivate(client_without_user: FlaskClient):
    r = client_without_user.get("/public_api/words")
    print(r.get_json())
    words_wth_paging = WordWithFieldsWithPaging(**r.get_json()["response"])
    assert WORD_NEW_TITLE not in [x.title for x in words_wth_paging.data]


def test_reactive_word(client_from_admin: FlaskClient):
    r = client_from_admin.post(
        f"/private_api/words/{WORD_ID}/deactivate",
    )
    assert r.status_code == 200


def test_list_word_from_public_after_reactivate(
    client_without_user: FlaskClient, word_create: WordCreate
):
    r = client_without_user.get("/public_api/words")
    print(r.get_json())
    words_wth_paging = WordWithFieldsWithPaging(**r.get_json()["response"])
    assert WORD_NEW_TITLE in [x.title for x in words_wth_paging.data]


def test_delete_word():
    """just to clean up"""
    WordService.delete_word(item_id=WORD_ID)
    WordService.delete_word(item_id=WORD_ID_TO_MERGE)


def test_delete_user(user_one: User, user_two: User):
    """just to clean up"""
    UserService.delete_user(item_id=user_one.id)
    UserService.delete_user(item_id=user_two.id)
