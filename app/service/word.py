from app.casbin.role_definition import ResourceDomainEnum, ResourceRightsEnum
from app.db.models import models
from app.db.database import get_db
import app.repo.word as WordRepo
import app.repo.field_version as FieldVersionRepo
import app.repo.suggestion as SuggestionRepo
import app.repo.user as UserRepo
from app.schemas.field_version import FieldEnum, FieldVersionCreate, FieldVersion
from app.schemas.suggestion import SuggestionCreate, Suggestion
from app.schemas.word import WordCreate, WordQuery, WordWithFields, WordWithFieldsWithPaging
from app.schemas.user import User
from app.casbin.enforcer import casbin_enforcer
from app.casbin.resource_id_converter import get_resource_id_from_item_id
from sqlalchemy.orm import Session


def _create_field_version_and_add_policy(
    db: Session, word_id: str, content: str, actor: User
) -> models.FieldVersion:
    db_field_version = FieldVersionRepo.create(
        db=db,
        item_create=FieldVersionCreate(
            word_id=word_id,
            field=FieldEnum.explanation,
            content=content,
        ),
        actor=actor,
    )
    casbin_enforcer.add_policy(
        actor.id,
        get_resource_id_from_item_id(
            item_id=db_field_version.id, domain=ResourceDomainEnum.field_versions
        ),
        ResourceRightsEnum.own_field_version,
    )
    return db_field_version


def create_word(item_create: WordCreate, actor: User) -> WordWithFields:
    with get_db() as db:
        db_word = WordRepo.create(db=db, item_create=item_create, actor=actor)
        casbin_enforcer.add_policy(
            actor.id,
            get_resource_id_from_item_id(
                item_id=db_word.id, domain=ResourceDomainEnum.words
            ),
            ResourceRightsEnum.own_word,
        )

        word_with_fields = WordWithFields.from_orm(db_word)

        if item_create.explanation:
            db_field_version = _create_field_version_and_add_policy(
                db=db, word_id=db_word.id, content=item_create.explanation, actor=actor
            )
            word_with_fields.explanation = db_field_version.content
        if item_create.usage:
            db_field_version = _create_field_version_and_add_policy(
                db=db, word_id=db_word.id, content=item_create.usage, actor=actor
            )
            word_with_fields.usage = db_field_version.content
        if item_create.tags:
            db_field_version = _create_field_version_and_add_policy(
                db=db, word_id=db_word.id, content=item_create.tags, actor=actor
            )
            word_with_fields.tags = db_field_version.content
        if item_create.pronunciation:
            db_field_version = _create_field_version_and_add_policy(
                db=db,
                word_id=db_word.id,
                content=item_create.pronunciation,
                actor=actor,
            )
            word_with_fields.pronunciation = db_field_version.content

        # and add casbin rules.. well it is a lot of things to do..
    return word_with_fields


def _update_fields_of_an_empty_word(db: Session, word_with_fields: WordWithFields) -> None:
    db_field_versions = FieldVersionRepo.get_all_field_versions_of_a_word(
        db=db, word_id=word_with_fields.id
    )
    # create a hashmap..
    field_to_content_and_vote = {}
    for fv in db_field_versions:  # it is already sorted based on creatio
        if fv.field not in field_to_content_and_vote:
            field_to_content_and_vote[fv.field] = (fv.content, fv.up_votes)
            setattr(word_with_fields, fv.field, fv.content)
        else:
            # well it is sorted by the most up votes..
            if fv.up_votes > field_to_content_and_vote[fv.field][1]:
                field_to_content_and_vote[fv.field] = (fv.content, fv.up_votes)
                setattr(word_with_fields, fv.field, fv.content)


def list_word_by_title(query: WordQuery) -> WordWithFieldsWithPaging:
    """used when user search for 62"""

    with get_db() as db:
        # retrieve the word
        db_words, paging = WordRepo.get_all(
            db=db, query_pagination=query
        )

        words_with_fields = [WordWithFields.from_orm(db_word) for db_word in db_words]

        for w in words_with_fields:
            _update_fields_of_an_empty_word(
                db=db, word_with_fields=w
            )

    return WordWithFieldsWithPaging(
        data=words_with_fields,
        paging=paging
    )


def delete_word(item_id) -> None:
    # for test purpose, there will not be 

    # delete suggestions
    # remove the casbin policies

    # delete fv
    # remove the casbin policies

    # delete word
    # remove the casbin policies
    pass



        
