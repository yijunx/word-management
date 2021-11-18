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


def list_admin_user(query_pagination: QueryPagination):
    with get_db() as db:
        admin_user_ids = CasbinRepo.get_all_admin_user_ids(query_pagination)
        # now we can just return the admin users..



