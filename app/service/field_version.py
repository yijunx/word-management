from datetime import datetime, timezone
from app.casbin.role_definition import (
    ResourceActionsEnum,
    ResourceDomainEnum,
    ResourceRightsEnum,
)
from app.db.database import get_db
from app.db.models.models import FieldVersion as FieldVersionORM
from app.exceptions.general_exceptions import NotAuthorized
import app.repo.field_version as FieldVersionRepo
import app.repo.vote as VoteRepo
import app.repo.suggestion as SuggestionRepo
from app.schemas.field_version import (
    FieldVersionCreate,
    FieldVersion,
    FieldVersionPatch,
    FieldVersionQuery,
    FieldVersionWithPaging,
)
from app.schemas.vote import Vote
from app.schemas.user import User

# from app.casbin.enforcer import casbin_enforcer
from app.casbin.resource_id_converter import get_resource_id_from_item_id
from app.schemas.vote import VoteCreate


def create_field_version(item_create: FieldVersionCreate, actor: User) -> FieldVersion:
    with get_db() as db:
        db_field_version = FieldVersionRepo.create(
            db=db, item_create=item_create, actor=actor
        )
        # casbin_enforcer.add_policy(
        #     actor.id,
        #     get_resource_id_from_item_id(
        #         item_id=db_field_version.id,
        #         domain=ResourceDomainEnum.field_versions,
        #     ),
        #     ResourceRightsEnum.own_field_version,
        # )
        field_version = FieldVersion.from_orm(db_field_version)
    return field_version


def list_field_version(
    query: FieldVersionQuery, creator: User = None, actor: User = None
) -> FieldVersionWithPaging:
    """
    if actor is there, we can show if the actor has voted for it or not
    if creator is there, this funciton only shows field version created
    by the creator
    """
    with get_db() as db:
        db_field_versions, paging = FieldVersionRepo.get_all(
            db=db, query_pagination=query, creator=creator
        )
        field_versions = [
            FieldVersion.from_orm(db_field_version)
            for db_field_version in db_field_versions
        ]
        if actor:
            # check the vote...
            votes = VoteRepo.get_all(
                db=db, version_ids=[x.id for x in field_versions], user_id=actor.id
            )
            votes_dict = {x.id: Vote.from_orm(x) for x in votes}
            # now append votes into to field_versions
            for f in field_versions:
                if f.id in votes_dict:
                    f.vote_up = votes_dict[f.id].vote_up
    return FieldVersionWithPaging(data=field_versions, paging=paging)


def update_field_version_content(
    item_patch: FieldVersionPatch, item_id: str, actor: User, is_admin: bool
) -> FieldVersion:
    with get_db() as db:
        db_item = FieldVersionRepo.get(db=db, item_id=item_id)

        if not is_admin:
            if db_item.created_by != actor.id:
                raise NotAuthorized(
                    actor=actor,
                    resource_id_or_domain=ResourceDomainEnum.suggestions,
                    action=ResourceActionsEnum.update_field_version_content,
                )
        db_item.modified_at = datetime.now(timezone.utc)
        db_item.content = item_patch.content
        item = FieldVersion.from_orm(db_item)

    return item


def accept_suggestion_to_my_version(
    item_id: str, suggestion_id: str, actor: User
) -> None:
    with get_db() as db:
        db_suggestion = SuggestionRepo.get(db=db, item_id=suggestion_id)
        db_field_version: FieldVersionORM = db_suggestion.field_version
        if db_field_version.id == item_id and db_field_version.created_by == actor.id:
            db_suggestion.accepted = True
        else:
            raise Exception("suggestion and item id not match")


def vote(item_id: str, vote_create: VoteCreate, actor: User) -> None:
    with get_db() as db:
        db_vote = VoteRepo.create(
            db=db, item_create=vote_create, actor=actor, version_id=item_id
        )
        # if the db_vote does not raise exception (already voted)
        FieldVersionRepo.vote(db=db, item_id=item_id, vote_up=db_vote.vote_up)


def unvote(item_id: str, actor: User):
    with get_db() as db:
        db_vote = VoteRepo.delete(db=db, version_id=item_id, user_id=actor.id)
        FieldVersionRepo.unvote(db=db, item_id=item_id, vote_up=db_vote.vote_up)


def activate_or_deactive_field_version(item_id: str, actor: User) -> None:
    with get_db() as db:
        db_item = FieldVersionRepo.get(db=db, item_id=item_id)
        db_item.active = not db_item.active
        db_item.modified_at = datetime.now(timezone.utc)
