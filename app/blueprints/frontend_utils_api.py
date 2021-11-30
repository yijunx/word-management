from flask import Blueprint
from app.util.app_logging import get_logger
from app.schemas.word import DialectEnum


bp = Blueprint(
    name="frontend_utils_bp",
    import_name=__name__,
    url_prefix="/public_api/words_frontend_utils",
)
logger = get_logger(__name__)


@bp.route("/dialects", methods=["GET"])
def list_dialects():
    """used to show entries or searches, user login is not required.
    thus in this endpoint, we do not know the user, and does not require casbin

    """
    return {
        "response": [x.value for x in DialectEnum],
        "success": True,
        "message": None,
    }
