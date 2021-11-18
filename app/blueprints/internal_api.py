# this is the internal api
from flask import Blueprint, request
from flask_pydantic import validate
from app.util.app_logging import get_logger
from app.casbin.decorator import authorize
from app.casbin.role_definition import ResourceDomainEnum, ResourceActionsEnum
from app.schemas.user import User
import app.service.suggestion as SuggestionService
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
@bp.route("/admin_users", method=["POST"])
@validate()
def create_admin(body: User):
    pass


# remove admin user
@bp.route("/admin_users/<user_id>", method=["DELETE"])
@validate()
def remove_admin():
    pass



# list admin user
@bp.route("/admin_users", method=["GET"])
@validate()
def list_admin():
    pass

