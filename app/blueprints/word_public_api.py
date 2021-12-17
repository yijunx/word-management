from flask import Blueprint
from flask_pydantic import validate
from app.exceptions.word import TagDoesNotExist, WordDoesNotExist
from app.util.app_logging import get_logger
from app.schemas.word import WordQuery
import app.service.word as WordService
from app.util.response_util import create_response


bp = Blueprint(
    name="word_public_bp", import_name=__name__, url_prefix="/api/public/words"
)
logger = get_logger(__name__)


@bp.route("", methods=["GET"])
@validate()
def list_words(query: WordQuery):
    """used to show entries or searches, user login is not required.
    thus in this endpoint, we do not know the user, and does not require casbin

    """
    try:
        words_with_paging = WordService.list_word(
            query=query, active_only=True, include_merged=False
        )
    except TagDoesNotExist as e:
        return create_response(
            success=False, message=e.message, status_code=e.status_code
        )
    except Exception as e:
        logger.debug(e, exc_info=True)
        return create_response(success=False, message=str(e), status_code=500)
    return create_response(response=words_with_paging)


@bp.route("/<item_id>", methods=["GET"])
@validate()
def get_word(item_id: str):
    """get the word"""
    try:
        r = WordService.get_word(item_id=item_id)
    except WordDoesNotExist as e:
        return create_response(
            success=False, message=e.message, status_code=e.status_code
        )
    except Exception as e:
        logger.debug(e, exc_info=True)
        return create_response(success=False, message=str(e), status_code=500)
    return create_response(response=r)


@bp.route("/<item_id>/contributors", methods=["GET"])
@validate()
def get_word_contributors(item_id: str):
    """get the contributors of the word"""
    try:
        r = WordService.get_contributor_of_word(item_id=item_id)
    except WordDoesNotExist as e:
        return create_response(
            success=False, message=e.message, status_code=e.status_code
        )
    except Exception as e:
        logger.debug(e, exc_info=True)
        return create_response(success=False, message=str(e), status_code=500)
    return create_response(response=r)
