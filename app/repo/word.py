from typing import List, Tuple
from sqlalchemy.sql.expression import and_, or_
from app.schemas.pagination import ResponsePagination
from app.db.models import models
from sqlalchemy.orm import Session
from app.schemas.user import User
from app.schemas.word import WordCreate, WordQuery
from uuid import uuid4
from sqlalchemy.exc import IntegrityError
from app.exceptions.word import WordAlreadyExist, WordDoesNotExist
from datetime import datetime, timezone
from app.repo.util import translate_query_pagination
import app.repo.tag as TagRepo


def create(db: Session, item_create: WordCreate, actor: User) -> models.Word:

    now = datetime.now(timezone.utc)

    db_item = models.Word(
        id=str(uuid4()),
        title=item_create.title,
        locked=False,
        # merged_to not there when creation, let it be NULL in db
        dialect=item_create.dialect,
        created_at=now,
        modified_at=now,
        created_by=actor.id,
        active=True,
    )
    db.add(db_item)
    try:
        db.flush()
    except IntegrityError:
        db.rollback()
        raise WordAlreadyExist(
            word_title=item_create.title, dialect=item_create.dialect
        )
    return db_item


def delete_all(db: Session) -> None:
    db.query(models.Word).delete()


def delete(db: Session, item_id: str):
    db_item = db.query(models.Word).filter(models.Word.id == item_id).first()
    if not db_item:
        raise WordDoesNotExist(word_id=item_id)
    db.delete(db_item)


def get(db: Session, item_id: str) -> models.Word:
    db_item = db.query(models.Word).filter(models.Word.id == item_id).first()
    if not db_item:
        raise WordDoesNotExist(word_id=item_id)
    return db_item


def get_all(
    db: Session,
    query_pagination: WordQuery,
    active_only: bool = True,
    include_merged: bool = False,
    creator: User = None,
) -> Tuple[List[models.Word], ResponsePagination]:

    query = db.query(models.Word)

    if not include_merged:
        query = query.filter(models.Word.merged_to == None)

    if creator:
        query = query.filter(models.Word.created_by == creator.id)

    # search based on tag or title
    # well.. word does not have TAG!!!!!
    # TAG is in the fields version
    # well this is bad
    # if query_pagination.tag:  # well this is doing a full scan... this is bad..
    #     query = query.filter(models.Word.tag.ilike(f"%#{query_pagination.tag}%"))
    # well tag must be separately managed in the tag table
    # and tags points to words
    if query_pagination.title:  # full text search we may need to use elastic
        # well the ilike here is a full table scan..
        # it is pretty bad
        query = query.filter(models.Word.title.contains(query_pagination.title))

    if query_pagination.tag:
        db_tag = TagRepo.get_by_content(db=db, content=query_pagination.tag)
        query = (
            db.query(models.Word)
            .join(models.Word.tags)
            .filter(models.TagWordAssociation.tag_id == db_tag.id)
        )
        # query = query.filter(models.Word.tags.any(models.Tag.id == db_tag.id))

    if query_pagination.dialect:
        query = query.filter(models.Word.dialect == query_pagination.dialect)

    if active_only:
        query = query.filter(models.Word.active == True)

    total = query.count()
    limit, offset, paging = translate_query_pagination(
        query_pagination=query_pagination, total=total
    )

    db_items = query.order_by(models.Word.title).limit(limit).offset(offset).all()
    paging.page_size = len(db_items)
    return db_items, paging
