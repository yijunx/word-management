import pytest
from sqlalchemy.orm.session import Session
from app.db.models.models import User
import app.repo.word as wordRepo
import app.repo.field_version as FieldVersionRepo
import app.repo.suggestion as SuggestionRepo
import app.repo.user as UserRepo
from app.schemas.field_version import FieldEnum, FieldVersionCreate
from app.schemas.suggestion import SuggestionCreate
from app.schemas.word import WordCreate

WORD_ID = ""
VERSION_IDS = []


def test_create_user(db: Session, user_one: User):
    db_item = UserRepo.create(db=db, actor=user_one)
    assert db_item.name == user_one.name


def test_create_word(db: Session, user_one: User, word_create: WordCreate):
    db_item = wordRepo.create(db=db, item_create=word_create, actor=user_one)
    global WORD_ID
    WORD_ID = db_item.id
    assert db_item.creator.id == user_one.id
    assert db_item.created_by == user_one.id


def test_create_versions(db: Session, user_one: User, word_create: WordCreate):
    db_exp = FieldVersionRepo.create(
        db=db,
        item_create=FieldVersionCreate(
            word_id=WORD_ID,
            field=FieldEnum.explanation,
            content=word_create.explanation,
        ),
        actor=user_one,
    )
    db_usg = FieldVersionRepo.create(
        db=db,
        item_create=FieldVersionCreate(
            word_id=WORD_ID, field=FieldEnum.usage, content=word_create.usage
        ),
        actor=user_one,
    )
    db_tag = FieldVersionRepo.create(
        db=db,
        item_create=FieldVersionCreate(
            word_id=WORD_ID, field=FieldEnum.tags, content=word_create.tags
        ),
        actor=user_one,
    )
    db_pro = FieldVersionRepo.create(
        db=db,
        item_create=FieldVersionCreate(
            word_id=WORD_ID,
            field=FieldEnum.pronunciation,
            content=word_create.pronunciation,
        ),
        actor=user_one,
    )

    global VERSION_IDS
    VERSION_IDS = [db_usg.id, db_exp.id, db_tag.id, db_pro.id]

    assert db_usg.word_id == WORD_ID
    assert db_exp.content == word_create.explanation
    assert db_tag.created_by == user_one.id
    assert db_pro.active == True


def test_delete_versions(db: Session):
    for version_id in VERSION_IDS:
        FieldVersionRepo.delete(db=db, item_id=version_id)


def test_delete_word(db: Session):
    wordRepo.delete(db=db, item_id=WORD_ID)


def test_delete_user(db: Session, user_one: User):
    UserRepo.delete(db=db, item_id=user_one.id)
