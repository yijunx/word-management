from datetime import datetime, timezone
from typing import List

import casbin
from app.casbin.role_definition import ResourceDomainEnum, ResourceRightsEnum
from app.db.models import models
from app.db.database import get_db
import app.repo.word as WordRepo
import app.repo.field_version as FieldVersionRepo
import app.repo.suggestion as SuggestionRepo
import app.repo.casbin as CasbinRepo
from app.schemas.field_version import FieldEnum, FieldVersionCreate
from app.schemas.word import (
    Word,
    WordContribution,
    WordCreate,
    WordPatch,
    WordQuery,
    WordWithFields,
    WordWithFieldsWithPaging,
)
from app.schemas.user import User, UserInContribution
from app.casbin.enforcer import casbin_enforcer
from app.casbin.resource_id_converter import get_resource_id_from_item_id
from sqlalchemy.orm import Session


def _create_field_version_and_add_policy(
    db: Session, word_id: str, content: str, actor: User, field: FieldEnum
) -> models.FieldVersion:
    db_field_version = FieldVersionRepo.create(
        db=db,
        item_create=FieldVersionCreate(
            word_id=word_id,
            field=field,
            content=content,
        ),
        actor=actor,
    )
    casbin_enforcer.add_policy(
        actor.id,
        get_resource_id_from_item_id(
            # for field version resource name,
            # word id is added for ease of deleting
            item_id=db_field_version.id,
            domain=ResourceDomainEnum.field_versions,
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
                db=db,
                word_id=db_word.id,
                content=item_create.explanation,
                actor=actor,
                field=FieldEnum.explanation,
            )
            word_with_fields.explanation = db_field_version.content
        if item_create.usage:
            db_field_version = _create_field_version_and_add_policy(
                db=db,
                word_id=db_word.id,
                content=item_create.usage,
                actor=actor,
                field=FieldEnum.usage,
            )
            word_with_fields.usage = db_field_version.content
        if item_create.tags:
            db_field_version = _create_field_version_and_add_policy(
                db=db,
                word_id=db_word.id,
                content=item_create.tags,
                actor=actor,
                field=FieldEnum.tags,
            )
            word_with_fields.tags = db_field_version.content
        if item_create.pronunciation:
            db_field_version = _create_field_version_and_add_policy(
                db=db,
                word_id=db_word.id,
                content=item_create.pronunciation,
                actor=actor,
                field=FieldEnum.pronunciation,
            )
            word_with_fields.pronunciation = db_field_version.content

        # and add casbin rules.. well it is a lot of things to do..
    return word_with_fields


def _update_fields_of_an_empty_word(
    db: Session, word_with_fields: WordWithFields
) -> None:
    """this function updates word_with_fields inplace"""
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


def list_word(
    query: WordQuery,
    creator: User = None,
    active_only: bool = True,
    include_merged: bool = False,
) -> WordWithFieldsWithPaging:
    """used when user search for 62"""

    with get_db() as db:
        # retrieve the word
        db_words, paging = WordRepo.get_all(
            db=db,
            query_pagination=query,
            creator=creator,
            active_only=active_only,
            include_merged=include_merged,
        )

        words_with_fields = [WordWithFields.from_orm(db_word) for db_word in db_words]

        for w in words_with_fields:
            _update_fields_of_an_empty_word(db=db, word_with_fields=w)

    return WordWithFieldsWithPaging(data=words_with_fields, paging=paging)


def get_word(item_id: str) -> WordWithFields:
    """when viewer goes into the word"""
    with get_db() as db:
        db_word = WordRepo.get(db=db, item_id=item_id)
        word_with_fields = WordWithFields.from_orm(db_word)
        _update_fields_of_an_empty_word(db=db, word_with_fields=word_with_fields)

    return word_with_fields


def activate_or_deactive_word(item_id: str, actor: User) -> None:
    with get_db() as db:
        db_word = WordRepo.get(db=db, item_id=item_id)
        if db_word.merged_to is not None:
            db_word.active = not db_word.active
            db_word.modified_at = datetime.now(timezone.utc)
            db_word.deactivated_by = actor.id


def lock_or_unlock_word(item_id: str, actor: User) -> None:
    with get_db() as db:
        db_word = WordRepo.get(db=db, item_id=item_id)
        if db_word.merged_to is not None:
            db_word.locked = not db_word.locked
            db_word.locked_by = actor.id
            db_word.modified_at = datetime.now(timezone.utc)


def merge_word(item_id: str, merged_to_word_id: str, actor: User) -> None:
    with get_db() as db:
        db_word = WordRepo.get(db=db, item_id=item_id)
        merged_to_db_word = WordRepo.get(db=db, item_id=merged_to_word_id)
        if db_word.merged_to is not None and merged_to_db_word.merged_to is not None:
            merged_to_db_word.modified_at = datetime.now(timezone.utc)
            db_word.merged_to = merged_to_db_word.id
            db_word.merged_at = datetime.now(timezone.utc)
            db_word.merged_by = actor.id
            db_word.active = False
            db_word.locked = True
            db_word.locked_by = actor.id

            # need to update the field versions and suggestions also
            FieldVersionRepo.replace_word_id(
                db=db, old_word_id=db_word.id, new_word_id=merged_to_word_id
            )
            SuggestionRepo.replace_word_id(
                db=db, old_word_id=db_word.id, new_word_id=merged_to_word_id
            )


def get_contributor_of_word(item_id: str) -> WordContribution:
    with get_db() as db:
        db_word = WordRepo.get(db=db, item_id=item_id)
        contributors_ids = set()
        contributors = []
        # add creator
        contributors.append(db_word.creator)
        contributors_ids.add(db_word.created_by)

        # add field versions creators
        for fv in db_word.field_versions:
            if fv.created_by not in contributors_ids:
                contributors.append(fv.creator)
                contributors_ids.add(fv.created_by)
            for sug in fv.suggestions:
                if sug.created_by not in contributors_ids:
                    contributors.append(sug.creator)
                    contributors.append(db_word.creator)

        contributors = [UserInContribution.from_orm(x) for x in contributors]
    return WordContribution(data=contributors)


def update_word_title(body: WordPatch, actor: User, item_id: str) -> Word:
    """used when the word owner update word title"""

    with get_db() as db:
        db_word = WordRepo.get(db=db, item_id=item_id)
        if db_word.locked or db_word.merged_to:
            raise Exception("This word is locked")
        if body.title:
            db_word.title = body.title
            db_word.modified_at = datetime.now(timezone.utc)
        word = Word.from_orm(db_word)
    return word


def delete_word(item_id) -> None:
    """for test purpose"""
    with get_db() as db:
        word = WordRepo.get(db=db, item_id=item_id)
        for field_version in word.field_versions:
            for suggestion in field_version.suggestions:
                CasbinRepo.delete_policies_by_resource_id(
                    db=db,
                    resource_id=get_resource_id_from_item_id(
                        item_id=suggestion.id, domain=ResourceDomainEnum.suggestions
                    ),
                )
            CasbinRepo.delete_policies_by_resource_id(
                db=db,
                resource_id=get_resource_id_from_item_id(
                    item_id=field_version.id, domain=ResourceDomainEnum.field_versions
                ),
            )
        CasbinRepo.delete_policies_by_resource_id(
            db=db,
            resource_id=get_resource_id_from_item_id(
                item_id=item_id, domain=ResourceDomainEnum.words
            ),
        )
        SuggestionRepo.delete_all(db=db, word_id=item_id)
        FieldVersionRepo.delete_all(db=db, word_id=item_id)
        WordRepo.delete(db=db, item_id=item_id)
