from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.exc import IntegrityError
from app.db.models import models
from sqlalchemy.orm import Session


def create(db: Session, word_id: str, tag_id: str) -> models.TagWordAssociation:
    """
    """
    db_item = models.TagWordAssociation(
        tag_id=tag_id,
        word_id=word_id
    )
    db.add(db_item)
    try:
        db.flush()
    except IntegrityError:
        db.rollback()
    return db_item