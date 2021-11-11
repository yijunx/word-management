from typing import List, Tuple
from sqlalchemy.sql.expression import and_, or_
from app.schemas.pagination import ResponsePagination
from app.db.models import models
from sqlalchemy.orm import Session
from app.schemas.user import User
from app.schemas.suggestion import SuggestionCreate, SuggestionQuery
from uuid import uuid4
from datetime import datetime, timezone
from app.repo.util import translate_query_pagination


def create(
    db: Session, item_create: SuggestionCreate, actor: User
) -> models.Suggestion:

    now = datetime.now(timezone.utc)

    db_item = models.Suggestion(
        id=str(uuid4()),
        word_id=item_create.word_id,
        version_id=item_create.version_id,
        content=item_create.content,  # can be updated by the owner or admin
        accepted=False,
        created_at=now,
        modified_at=now,
        created_by=actor.id,
        active=True,
    )
    db.add(db_item)
    db.flush()
    return db_item


def delete_all(db: Session) -> None:
    db.query(models.Suggestion).delete()


def delete(db: Session, item_id: str) -> None:
    db_item = (
        db.query(models.Suggestion).filter(models.Suggestion.id == item_id).first()
    )
    if not db_item:
        raise Exception("suggestion does not exist")
    db.delete(db_item)


def get(db: Session, item_id: str) -> models.Suggestion:
    db_item = (
        db.query(models.Suggestion).filter(models.Suggestion.id == item_id).first()
    )
    if not db_item:
        raise Exception("suggestion does not exist")
    return db_item


def get_all(
    db: Session, query_pagination: SuggestionQuery, active_only: bool = True
) -> Tuple[List[models.Suggestion], ResponsePagination]:

    query = db.query(models.Suggestion)

    query = query.filter(models.Suggestion.word_id == query_pagination.word_id)

    if query_pagination.version_id:
        query = query.filter(
            models.Suggestion.version_id == query_pagination.version_id
        )

    if active_only:
        query = query.filter(models.Suggestion.active == True)

    total = query.count()
    limit, offset, paging = translate_query_pagination(
        query_pagination=query_pagination, total=total
    )

    db_items = (
        query.order_by(models.Suggestion.created_at.desc())
        .limit(limit)
        .offset(offset)
        .all()
    )
    paging.page_size = len(db_items)
    return db_items, paging
