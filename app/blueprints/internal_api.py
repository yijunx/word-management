# this is the internal api
from flask import Blueprint
from flask_pydantic import validate
from app.schemas.pagination import QueryPagination
from app.util.app_logging import get_logger
from app.schemas.user import User, UserPatch
import app.service.user as UserService
from app.util.response_util import create_response


bp = Blueprint(
    name="internal_bp",
    import_name=__name__,
    url_prefix="/internal_api",
)

logger = get_logger(__name__)
# internal api is for internal commication
# internal communication does not require token


# liveness

# add admin user, no need to check token here
# as the communication is internal
@bp.route("/admin_users", methods=["POST"])
@validate()
def create_admin(body: User):
    UserService.add_admin_user(user=body)
    return create_response(message="admin user created in word management")


# remove admin user
@bp.route("/admin_users/<user_id>", methods=["DELETE"])
@validate()
def remove_admin(user_id: str):
    UserService.remove_admin_user(user_id=user_id)
    return create_response(message="admin user removed in word management")


# list admin user
@bp.route("/admin_users/<user_id>", methods=["GET"])
@validate()
def get_admin(user_id: str):
    r = UserService.get_admin_user(user_id=user_id)
    return create_response(response=r)


# list admin user
@bp.route("/admin_users", methods=["GET"])
@validate()
def list_admin(query: QueryPagination):
    r = UserService.list_admin_user(query_pagination=query)
    return create_response(response=r)


# modify user name or email
@bp.route("/users/<user_id>", methods=["PATCH"])
@validate()
def update_user_info(user_id: str, body: UserPatch):
    UserService.patch_user(item_id=user_id, user_patch=body)
    return create_response(message="user updated")
