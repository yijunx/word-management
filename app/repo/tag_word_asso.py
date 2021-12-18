from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql.expression import and_
from app.db.models import models
from sqlalchemy.orm import Session


def create(db: Session, word_id: str, tag_id: str) -> models.TagWordAssociation:
    """ """
    db_item = models.TagWordAssociation(tag_id=tag_id, word_id=word_id)
    db.add(db_item)
    try:
        db.flush()
    except IntegrityError:
        db.rollback()
    return db_item


def get_or_create(db: Session, word_id: str, tag_id: str) -> models.TagWordAssociation:
    db_item = (
        db.query(models.TagWordAssociation)
        .filter(
            and_(
                models.TagWordAssociation.word_id == word_id,
                models.TagWordAssociation.tag_id == tag_id,
            )
        )
        .first()
    )
    if db_item:
        return db_item
    else:
        return create(db=db, word_id=word_id, tag_id=tag_id)


def delete_all(db: Session, word_id: str = None, tag_id: str = None) -> None:

    query = db.query(models.TagWordAssociation)

    if word_id:
        query = query.filter(models.TagWordAssociation.word_id == word_id)

    if tag_id:
        query = query.filter(models.TagWordAssociation.tag_id == tag_id)

    query.delete(synchronize_session=False)
