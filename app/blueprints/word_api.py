from flask import Blueprint, request
from flask_pydantic import validate
from app.util.app_logging import get_logger
from app.casbin.decorator import authorize
from app.casbin.role_definition import ResourceDomainEnum, ResourceActionsEnum
from app.schemas.user import User
from app.schemas.word import WordCreate, WordQuery
import app.service.word as WordService
from app.util.response_util import create_response
from app.exceptions.word import WordAlreadyExist, WordDoesNotExist


bp = Blueprint(name="words_bp", import_name=__name__, url_prefix="/api/words")
logger = get_logger(__name__)


@bp.route("", methods=["POST"])
@authorize(require_casbin=False)
@validate()
def create_word(body: WordCreate):
    actor: User = request.environ["actor"]
    try:
        word = WordService.create_word(
            item_create=body, actor=actor
        )
    except WordAlreadyExist as e:
        return create_response(success=False, message=e.message, status_code=e.http_code)
    except Exception as e:
        logger.debug(e, exc_info=True)
        return create_response(success=False, message=str(e), status_code=500)

    return create_response(
        response=word
    )



@bp.route("", methods=["GET"])
@validate()
def get_words(query: WordQuery):
    """used to show entries or searches, user login is not required.
    thus in this endpoint, we do not know the user, and does not require casbin
    """



    pass


@bp.route("", methods=["GET"])
@authorize(require_casbin=False)
@validate()
def get_my_words():
    """
    well this is get my words, so need to know who this is, thus user login,
    verification, auth headers is needed, but, no need to pass casbin"""
    actor: User = request.environ["actor"]