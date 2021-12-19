from flask import Blueprint
from app.util.app_logging import get_logger
from app.schemas.word import DialectEnum


bp = Blueprint(
    name="frontend_utils_bp",
    import_name=__name__,
    url_prefix="/api/public/words_frontend_utils",
)
logger = get_logger(__name__)


@bp.route("/dialects", methods=["GET"])
def list_dialects():
    """used to show entries or searches, user login is not required.
    thus in this endpoint, we do not know the user, and does not require casbin

    """
    response = [{"name": x.value} for x in DialectEnum]
    i = 0
    for x in response:
        x["id"] = i
        i = i + 1

    return {
        "response": response,
        "success": True,
        "message": None,
    }
