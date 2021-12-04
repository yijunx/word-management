from typing import List
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.exc import IntegrityError
from app.db.models import models
from sqlalchemy.orm import Session
import uuid

from app.exceptions.word import TagDoesNotExist


def create(db: Session, content: str) -> models.Tag:
    """ """
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
    db_item = db.query(models.Tag).filter(models.Tag.content == content).first()
    if not db_item:
        raise TagDoesNotExist(tag=content)
    return db_item


def delete(db: Session, tag_id: str) -> None:
    query = db.query(models.Tag).filter(models.Tag.id == tag_id)
    query.delete(synchronize_session=False)


def get_all(db: Session, word_id: str) -> List[models.Tag]:
    # query = query.filter(models.Word.tags.any(models.Tag.id == db_tag.id))
    query = (
        db.query(models.Tag)
        .join(models.Tag.words)
        .filter(models.TagWordAssociation.word_id == word_id)
    )
    #  .filter(models.TagWordAssociation.word_id == word_id)
    # query = db.query(models.Tag).filter(models.Tag.words.any(models.Word.id == word_id))
    db_items = query.order_by(models.Tag.content).all()
    return db_items
