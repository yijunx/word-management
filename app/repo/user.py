from typing import List, Tuple
from sqlalchemy.sql.expression import and_, or_
from app.schemas.pagination import ResponsePagination
from app.db.models import models
from sqlalchemy.orm import Session
from app.schemas.user import User
from uuid import uuid4
from datetime import datetime, timezone
from app.repo.util import translate_query_pagination


def create(db: Session, actor: User) -> models.User:
    """
    here the user already create himself
    with data from cookie
    there is no way other people create user for him/her
    """

    # now = datetime.now(timezone.utc)

    db_item = models.User(
        id=actor.id,
        name=actor.name,
        email=actor.email,
    )
    db.add(db_item)
    db.flush()
    return db_item


def delete_all(db: Session) -> None:
    db.query(models.User).delete()


def delete(db: Session, item_id: str) -> None:
    db_item = db.query(models.User).filter(models.User.id == item_id).first()
    if not db_item:
        raise Exception("user does not exist")
    db.delete(db_item)


def get(db: Session, item_id: str) -> models.User:
    db_item = db.query(models.User).filter(models.User.id == item_id).first()
    if not db_item:
        raise Exception("user does not exist")
    return db_item
