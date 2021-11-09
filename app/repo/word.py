from typing import List, Tuple, Union
from sqlalchemy.sql.expression import and_, or_
from app.schemas.pagination import QueryPagination, ResponsePagination
from app.db.models import models
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserPatch
from uuid import uuid4
from sqlalchemy.exc import IntegrityError


def create(db: Session, item_create: UserCreate) -> models.User:
    db_item = models.User(
        id=str(uuid4()),  # [let db create the id for us]
        name=item_create.name,
        created_at=item_create.created_at,
        email=item_create.email,
        login_method=item_create.login_method,
        salt=item_create.salt,
        hashed_password=item_create.hashed_password,
        email_verified=item_create.email_verified,
    )
    db.add(db_item)
    try:
        db.flush()
    except IntegrityError:
        db.rollback()
        raise UserEmailAlreadyExist(email=item_create.email)
    return db_item


def delete_all(db: Session) -> None:
    db.query(models.User).delete()