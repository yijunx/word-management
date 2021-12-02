from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.exc import IntegrityError
from app.db.models import models
from sqlalchemy.orm import Session
import uuid


def create(db: Session, content: str) -> models.Tag:
    """
    here the user already create himself
    with data from cookie
    there is no way other people create user for him/her
    """
    db_item = models.User(
        id=str(uuid.uuid4()),
        content=content
    )
    db.add(db_item)
    try:
        db.flush()
    except IntegrityError:
        db.rollback()
    return db_item


def get_or_create(db: Session, content: str) -> models.Tag:
    db_item = db.query(models.User).filter(content == content).first()
    if not db_item:
        db_item = create(db=db, content=content)
    return db_item


