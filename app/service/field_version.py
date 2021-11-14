from datetime import datetime, timezone
from app.casbin.role_definition import ResourceDomainEnum, ResourceRightsEnum
from app.db.database import get_db
import app.repo.word as WordRepo
import app.repo.field_version as FieldVersionRepo
import app.repo.suggestion as SuggestionRepo
import app.repo.user as UserRepo
import app.repo.casbin as CasbinRepo
from app.schemas.field_version import (
    FieldEnum,
    FieldVersionCreate,
    FieldVersion,
    FieldVersionPatch,
    FieldVersionQuery,
    FieldVersionWithPaging,
)
from app.schemas.suggestion import SuggestionCreate, Suggestion
from app.schemas.user import User
from app.casbin.enforcer import casbin_enforcer
from app.casbin.resource_id_converter import get_resource_id_from_item_id
from sqlalchemy.orm import Session


def create_field_version(item_create: FieldVersionCreate, actor: User) -> FieldVersion:
    with get_db() as db:
        db_field_version = FieldVersionRepo.create(
            db=db, item_create=item_create, actor=actor
        )
        casbin_enforcer.add_policy(
            actor.id,
            get_resource_id_from_item_id(
                item_id=db_field_version.id, domain=ResourceDomainEnum.field_versions
            ),
            ResourceRightsEnum.own_field_version,
        )
        field_version = FieldVersion.from_orm(db_field_version)
    return field_version


def list_field_version(
    query: FieldVersionQuery, creator: User = None
) -> FieldVersionWithPaging:
    with get_db() as db:
        db_field_versions, paging = FieldVersionRepo.get_all(
            db=db, query_pagination=query, creator=creator
        )
        field_versions = [
            FieldVersion.from_orm(db_field_version)
            for db_field_version in db_field_versions
        ]
    return FieldVersionWithPaging(data=field_versions, paging=paging)


def update_field_version_content(
    item_patch: FieldVersionPatch, item_id: str, actor: User
) -> FieldVersion:
    with get_db() as db:
        db_item = FieldVersionRepo.get(db=db, item_id=item_id)
        db_item.modified_at = datetime.now(timezone.utc)
        db_item.content = item_patch.content
        item = FieldVersion.from_orm(db_item)

    return item
