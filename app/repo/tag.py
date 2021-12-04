from typing import List
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.exc import IntegrityError
from app.db.models import models
from sqlalchemy.orm import Session
import uuid


def create(db: Session, content: str) -> models.Tag:
    """
    """
    db_item = models.Tag(id=str(uuid.uuid4()), content=content)
    db.add(db_item)
    try:
        db.flush()
    except IntegrityError:
        db.rollback()
    return db_item


def get_or_create(db: Session, content: str) -> models.Tag:
    db_item = db.query(models.Tag).filter(models.Tag.content == content).first()
    if not db_item:
        db_item = create(db=db, content=content)
    return db_item


def get_by_content(db: Session, content: str) -> models.Tag:
    db_item = db.query(models.Tag).filter(models.Tag.content == content)
    if not db_item:
        raise Exception("tag does not exist")
    return db_item



def delete(db: Session, tag_id: str) -> None:
    query = db.query(models.Tag).filter(models.Tag.id == tag_id)
    query.delete(synchronize_session=False)


def get_all(db: Session, word_id: str) -> List[models.Tag]:
    query = db.query(models.Tag).filter(models.Tag.words.any(models.Word.id == word_id))
    return query.all()
