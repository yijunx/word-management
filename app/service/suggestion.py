from datetime import datetime, timezone
from app.casbin.role_definition import (
    ResourceActionsEnum,
    ResourceDomainEnum,
    ResourceRightsEnum,
)
from app.db.database import get_db
from app.exceptions.general_exceptions import NotAuthorized
import app.repo.suggestion as SuggestionRepo
from app.schemas.suggestion import (
    SuggestionCreate,
    Suggestion,
    SuggestionPatch,
    SuggestionWithPaging,
    SuggestionQuery,
)
from app.schemas.user import User

# from app.casbin.enforcer import casbin_enforcer
from app.casbin.resource_id_converter import get_resource_id_from_item_id


def create_suggestion(item_create: SuggestionCreate, actor: User) -> Suggestion:
    with get_db() as db:
        db_suggestion = SuggestionRepo.create(
            db=db, item_create=item_create, actor=actor
        )
        # casbin_enforcer.add_policy(
        #     actor.id,
        #     get_resource_id_from_item_id(
        #         item_id=db_suggestion.id,
        #         domain=ResourceDomainEnum.suggestions,
        #     ),
        #     ResourceRightsEnum.own_suggestion,
        # )
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
        if not actor.is_suggestion_admin:
            if db_item.created_by != actor.id:
                raise NotAuthorized(
                    actor=actor,
                    resource_id_or_domain=get_resource_id_from_item_id(
                        item_id=item_id, domain=ResourceDomainEnum.suggestions
                    ),
                    action=ResourceActionsEnum.update_suggestion_content,
                )

        db_item.modified_at = datetime.now(timezone.utc)
        db_item.content = item_patch.content
        item = Suggestion.from_orm(db_item)

    return item


def activate_or_deactive_suggestion(item_id: str, actor: User) -> None:
    with get_db() as db:
        db_item = SuggestionRepo.get(db=db, item_id=item_id)
        db_item.active = not db_item.active
        db_item.modified_at = datetime.now(timezone.utc)
