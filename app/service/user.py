from app.schemas.casbin_rule import CasbinRuleWithPaging, CasbinRule
from app.schemas.user import User
from app.db.database import get_db
import app.repo.user as UserRepo
from app.casbin.enforcer import casbin_enforcer
import app.repo.casbin as CasbinRepo
from app.schemas.pagination import QueryPagination


def delete_user(item_id):
    with get_db() as db:
        UserRepo.delete(db=db, item_id=item_id)


def add_admin_user(user: User):
    casbin_enforcer.add_grouping_policy(user.id, "admin-role-id")


def remove_admin_user(user_id: str):
    casbin_enforcer.remove_grouping_policy(user_id, "admin-role-id")


def list_admin_user(query_pagination: QueryPagination) -> CasbinRuleWithPaging:
    with get_db() as db:
        db_casbin_rules, paging = CasbinRepo.get_all_admin_user_ids(
            db=db, admin_role_id="admin-role-id", query_pagination=query_pagination
        )
        casbin_rules = [CasbinRule.from_orm(x) for x in db_casbin_rules]
    return CasbinRuleWithPaging(data=casbin_rules, paging=paging)
