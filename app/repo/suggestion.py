from typing import List, Tuple
from sqlalchemy.sql.expression import and_, or_
from app.schemas.pagination import ResponsePagination
from app.db.models import models
from sqlalchemy.orm import Session
from app.schemas.suggestion import SuggestionCreate, SuggestionQuery
from uuid import uuid4
from datetime import datetime, timezone
from app.repo.util import translate_query_pagination


def create(
    db: Session, item_create: SuggestionCreate, actor: models.User
) -> models.Suggestion:

    now = datetime.now(timezone.utc)

    db_item = models.Suggestion(
        id=str(uuid4()),
        word_id=item_create.word_id,
        version_id=item_create.version_id,
        content=item_create.content,  # can be updated by the owner or admin
        
        created_at=now,
        modified_at=now,
        created_by=actor.id,
        up_votes=0,
        down_votes=0,
        active=True,  # only managed automatically
    )
    db.add(db_item)
    db.flush()
    return db_item