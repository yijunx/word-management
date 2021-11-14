from flask import Blueprint
from flask_pydantic import validate
from app.util.app_logging import get_logger
from app.schemas.field_version import FieldVersionQuery
import app.service.field_version as FieldVersionService
from app.util.response_util import create_response


bp = Blueprint(
    name="field_version_public_bp",
    import_name=__name__,
    url_prefix="/public_api/field_versions",
)
logger = get_logger(__name__)


@bp.route("", methods=["GET"])
@validate()
def get_field_versions(query: FieldVersionQuery):
    """used to show entries or searches, user login is not required.
    thus in this endpoint, we do not know the user, and does not require casbin
    """
    items_with_paging = FieldVersionService.list_field_version(query=query)
    return create_response(response=items_with_paging)
