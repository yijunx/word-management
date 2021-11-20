from datetime import datetime, timezone
from app.casbin.role_definition import ResourceDomainEnum, ResourceRightsEnum
from app.db.database import get_db
import app.repo.suggestion as SuggestionRepo
from app.schemas.suggestion import (
    SuggestionCreate,
    Suggestion,
    SuggestionPatch,
    SuggestionWithPaging,
    SuggestionQuery,
)
from app.schemas.user import User
from app.casbin.enforcer import casbin_enforcer
from app.casbin.resource_id_converter import get_resource_id_from_item_id


def create_suggestion(item_create: SuggestionCreate, actor: User) -> Suggestion:
    with get_db() as db:
        db_suggestion = SuggestionRepo.create(
            db=db, item_create=item_create, actor=actor
        )
        casbin_enforcer.add_policy(
            actor.id,
            get_resource_id_from_item_id(
                item_id=db_suggestion.id,
                domain=ResourceDomainEnum.suggestions,
            ),
            ResourceRightsEnum.own_suggestion,
        )
        sugguestion = Suggestion.from_orm(db_suggestion)
    return sugguestion


def list_suggestions(
    query: SuggestionQuery, creator: User = None
) -> SuggestionWithPaging:
    with get_db() as db:
        db_items, paging = SuggestionRepo.get_all(
            db=db, query_pagination=query, creator=creator
        )
        items = [Suggestion.from_orm(item) for item in db_items]
    return SuggestionWithPaging(data=items, paging=paging)


def update_suggesion_content(
    item_patch: SuggestionPatch, item_id: str, actor: User
) -> Suggestion:
    with get_db() as db:
        db_item = SuggestionRepo.get(db=db, item_id=item_id)
        db_item.modified_at = datetime.now(timezone.utc)
        db_item.content = item_patch.content
        item = Suggestion.from_orm(db_item)

    return item
