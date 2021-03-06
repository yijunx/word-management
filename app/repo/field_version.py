from typing import List, Tuple
from sqlalchemy.sql.expression import and_, or_
from app.schemas.pagination import ResponsePagination
from app.db.models import models
from sqlalchemy.orm import Session
from app.schemas.user import User
from app.schemas.field_version import FieldVersionCreate, FieldVersionQuery
from uuid import uuid4
from datetime import datetime, timezone
from app.repo.util import translate_query_pagination


def create(
    db: Session, item_create: FieldVersionCreate, actor: User
) -> models.FieldVersion:

    now = datetime.now(timezone.utc)

    db_item = models.FieldVersion(
        id=str(uuid4()),
        word_id=item_create.word_id,
        field=item_create.field,
        content=item_create.content,  # can be updated by the owner or admin
        created_at=now,
        modified_at=now,
        created_by=actor.id,
        up_votes=0,
        down_votes=0,
        active=True,  # only managed automatically
    )
    db.add(db_item)
    return db_item


def delete_all(db: Session, word_id: str = None) -> None:
    if word_id:
        db.query(models.FieldVersion).filter(
            models.FieldVersion.word_id == word_id
        ).delete()
    else:
        db.query(models.FieldVersion).delete()


def delete(db: Session, item_id: str) -> None:
    db_item = (
        db.query(models.FieldVersion).filter(models.FieldVersion.id == item_id).first()
    )
    if not db_item:
        raise Exception("field version does not exist")
    db.delete(db_item)


def replace_word_id(db: Session, old_word_id: str, new_word_id: str) -> None:
    """used when merge word"""
    db.query(models.FieldVersion).filter(
        models.FieldVersion.word_id == old_word_id
    ).update({"word_id": new_word_id})


def get(db: Session, item_id: str) -> models.FieldVersion:
    db_item = (
        db.query(models.FieldVersion).filter(models.FieldVersion.id == item_id).first()
    )
    if not db_item:
        raise Exception("field version does not exist")
    return db_item


def vote(db: Session, item_id: str, vote_up: bool) -> None:
    """this function will check if the vote_up is None or not"""
    if vote_up is not None:
        if vote_up:
            db.query(models.FieldVersion).filter(
                models.FieldVersion.id == item_id
            ).update({"up_votes": models.FieldVersion.up_votes + 1})
        else:
            db.query(models.FieldVersion).filter(
                models.FieldVersion.id == item_id
            ).update({"down_votes": models.FieldVersion.down_votes + 1})


def unvote(db: Session, item_id: str, vote_up: bool) -> None:
    """this function will check if the vote_up is None or not"""
    if vote_up is not None:
        if vote_up:
            db.query(models.FieldVersion).filter(
                models.FieldVersion.id == item_id
            ).update({"up_votes": models.FieldVersion.up_votes - 1})
        else:
            db.query(models.FieldVersion).filter(
                models.FieldVersion.id == item_id
            ).update({"down_votes": models.FieldVersion.down_votes - 1})


def get_all_field_versions_of_a_word(
    db: Session, word_id: str
) -> List[models.FieldVersion]:
    query = db.query(models.FieldVersion)
    query = query.filter(
        and_(models.FieldVersion.word_id == word_id, models.FieldVersion.active == True)
    )
    # old one on top
    # so if the vote are same, old version will dominate
    db_items = query.order_by(models.FieldVersion.created_at).all()

    # need to apply the manual pagination here...maybe at service level..
    return db_items


def get_all(
    db: Session,
    query_pagination: FieldVersionQuery,
    active_only: bool = True,
    creator: User = None,
) -> Tuple[List[models.FieldVersion], ResponsePagination]:

    query = db.query(models.FieldVersion)

    if query_pagination.word_id:
        query = query.filter(models.FieldVersion.word_id == query_pagination.word_id)

    if creator:
        query = query.filter(models.FieldVersion.created_by == creator.id)

    if active_only:
        query = query.filter(models.FieldVersion.active == True)

    if query_pagination.field:
        query = query.filter(models.FieldVersion.field == query_pagination.field)

    total = query.count()
    limit, offset, paging = translate_query_pagination(
        query_pagination=query_pagination, total=total
    )

    db_items = (
        query.order_by(models.FieldVersion.created_at.desc())
        .limit(limit)
        .offset(offset)
        .all()
    )
    paging.page_size = len(db_items)
    return db_items, paging
