from flask import Blueprint
from flask_pydantic import validate
from app.util.app_logging import get_logger
from app.schemas.suggestion import SuggestionQuery
import app.service.suggestion as SuggestionService
from app.util.response_util import create_response


bp = Blueprint(
    name="suggestion_public_bp",
    import_name=__name__,
    url_prefix="/public_api/suggestions",
)
logger = get_logger(__name__)


@bp.route("", methods=["GET"])
@validate()
def get_suggestions(query: SuggestionQuery):
    """used to show entries or searches, user login is not required.
    thus in this endpoint, we do not know the user, and does not require casbin
    """
    items_with_paging = SuggestionService.list_suggestions(query=query)
    return create_response(response=items_with_paging)