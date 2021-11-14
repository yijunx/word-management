from flask import Blueprint
from flask_pydantic import validate
from app.util.app_logging import get_logger
from app.schemas.word import WordQuery
import app.service.word as WordService
from app.util.response_util import create_response


bp = Blueprint(
    name="word_public_bp", import_name=__name__, url_prefix="/public_api/words"
)
logger = get_logger(__name__)


@bp.route("", methods=["GET"])
@validate()
def get_words(query: WordQuery):
    """used to show entries or searches, user login is not required.
    thus in this endpoint, we do not know the user, and does not require casbin

    """
    words_with_paging = WordService.list_word(query=query)
    return create_response(response=words_with_paging)
