from typing import Union, List
from app.exceptions.vote import VoteAlreadyExist, VoteDoesNotExist
from sqlalchemy.sql.expression import and_
from app.db.models import models
from sqlalchemy.orm import Session
from app.schemas.user import User
from app.schemas.vote import VoteCreate
from uuid import uuid4
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timezone


def create(
    db: Session, item_create: VoteCreate, actor: User, version_id: str
) -> models.Vote:

    now = datetime.now(timezone.utc)

    db_item = models.Vote(
        id=str(uuid4()),
        vote_up=item_create.vote_up,
        version_id=version_id,
        created_at=now,
        created_by=actor.id,
    )
    db.add(db_item)
    try:
        db.flush()
    except IntegrityError as e:
        db.rollback()
        raise VoteAlreadyExist(user_id=actor.id, version_id=version_id)
    return db_item


def get(db: Session, version_id: str, user_id: str) -> Union[None, models.Vote]:
    """used to check what the user voted
    returns none if not the user has not voted"""
    return (
        db.query(models.Vote)
        .filter(
            and_(
                models.Vote.version_id == version_id, models.Vote.created_by == user_id
            )
        )
        .first()
    )


def delete(db: Session, version_id: str, user_id: str) -> models.Vote:
    db_item = get(db=db, version_id=version_id, user_id=user_id)
    if db_item is None:
        raise VoteDoesNotExist(user_id=user_id, version_id=version_id)
    db.delete(db_item)
    return db_item


def get_all(db: Session, version_ids: List[str], user_id: str) -> List[models.Vote]:
    query = db.query(models.Vote).filter_by(
        and_(
            models.Vote.version_id.in_(version_ids),
            models.Vote.created_by == user_id
        )
    )
    return query.all()

