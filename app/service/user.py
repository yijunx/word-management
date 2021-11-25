from app.schemas.casbin_rule import CasbinRuleWithPaging, CasbinRule
from app.schemas.user import User, UserPatch
from app.db.database import get_db
import app.repo.user as UserRepo
from app.casbin.enforcer import casbin_enforcer
import app.repo.casbin as CasbinRepo
from app.schemas.pagination import QueryPagination
from app.config.app_config import conf


def delete_user(item_id: str):
    with get_db() as db:
        UserRepo.delete(db=db, item_id=item_id)


def patch_user(item_id: str, user_patch: UserPatch):
    with get_db() as db:
        db_user = UserRepo.get(db=db, item_id=item_id)
        if db_user:
            if user_patch.name:
                db_user.name = user_patch.name
            if user_patch.email:
                db_user.email = user_patch.email


def add_admin_user(user: User):
    casbin_enforcer.add_grouping_policy(user.id, conf.WORD_ADMIN_ROLE_ID)


def remove_admin_user(user_id: str):
    casbin_enforcer.remove_grouping_policy(user_id, conf.WORD_ADMIN_ROLE_ID)


def get_admin_user(user_id: str) -> CasbinRule:
    with get_db() as db:
        db_rule = CasbinRepo.get_grouping(
            db=db, role_id=conf.WORD_ADMIN_ROLE_ID, user_id=user_id
        )
        casbin_rule = CasbinRule.from_orm(db_rule)
    return casbin_rule


def list_admin_user(query_pagination: QueryPagination) -> CasbinRuleWithPaging:
    with get_db() as db:
        db_casbin_rules, paging = CasbinRepo.get_all_admin_user_ids(
            db=db,
            admin_role_id=conf.WORD_ADMIN_ROLE_ID,
            query_pagination=query_pagination,
        )
        casbin_rules = [CasbinRule.from_orm(x) for x in db_casbin_rules]
    return CasbinRuleWithPaging(data=casbin_rules, paging=paging)
