from flask import Blueprint, request
from flask_pydantic import validate
from app.util.app_logging import get_logger
from app.casbin.decorator import authorize
from app.casbin.role_definition import ResourceDomainEnum, ResourceActionsEnum
from app.schemas.user import User
from app.schemas.word import WordCreate, WordMerge, WordPatch, WordQuery
import app.service.word as WordService
from app.util.response_util import create_response
from app.exceptions.word import WordAlreadyExist, WordDoesNotExist


bp = Blueprint(
    name="word_private_bp", import_name=__name__, url_prefix="/api/private/words"
)
logger = get_logger(__name__)


@bp.route("", methods=["POST"])
@authorize(require_casbin=False)
@validate()
def create_word(body: WordCreate):
    actor: User = request.environ["actor"]
    try:
        word = WordService.create_word(item_create=body, actor=actor)
    except WordAlreadyExist as e:
        return create_response(
            success=False, message=e.message, status_code=e.status_code
        )
    except Exception as e:
        logger.debug(e, exc_info=True)
        return create_response(success=False, message=str(e), status_code=500)

    return create_response(response=word)


@bp.route("", methods=["GET"])
@authorize(require_casbin=False)
@validate()
def get_my_words(query: WordQuery):
    """
    well this is get my words, so need to know who this is, thus user login,
    verification, auth headers is needed, but, no need to pass casbin
    """
    actor, is_admin = request.environ["actor_info"]

    words_with_paging = WordService.list_word(
        query=query,
        actor=actor,
        is_admin=is_admin,
        active_only=False,
        include_merged=True,
    )
    return create_response(response=words_with_paging)


@bp.route("/<item_id>", methods=["PATCH"])
@authorize(require_casbin=False)
@validate()
def patch_my_word(item_id: str, body: WordPatch):
    """Currently it is only used to update word title"""
    actor, is_admin = request.environ["actor_info"]
    # admin can do anything???
    try:
        word = WordService.update_word_title(
            body=body, actor=actor, item_id=item_id, is_admin=is_admin
        )
    except WordDoesNotExist as e:
        return create_response(
            success=False, message=e.message, status_code=e.status_code
        )
    except Exception as e:
        logger.debug(e, exc_info=True)
        return create_response(success=False, message=str(e), status_code=500)
    return create_response(response=word)


@bp.route("/<item_id>/deactivate", methods=["POST"])
@authorize(action=ResourceActionsEnum.deactivate_word, domain=ResourceDomainEnum.words)
def activate_or_deactivate(item_id: str):
    """used for flipping the active flag, only admin user can do this"""
    actor: User = request.environ["actor"]
    try:
        WordService.activate_or_deactive_word(item_id=item_id, actor=actor)
    except WordDoesNotExist as e:
        return create_response(
            success=False, message=e.message, status_code=e.status_code
        )
    except Exception as e:
        logger.debug(e, exc_info=True)
        return create_response(success=False, message=str(e), status_code=500)
    return create_response(message="xxx")


@bp.route("/<item_id>/merge_into_another", methods=["POST"])
@authorize(action=ResourceActionsEnum.merge_word, domain=ResourceDomainEnum.words)
@validate()
def merge_into_another(body: WordMerge, item_id: str):
    """used for merge 2 words, using the title of the merged to ones,
    and change the word_id in the its field versions"""
    actor: User = request.environ["actor"]
    try:
        WordService.merge_word(
            item_id=item_id, merged_to_word_id=body.word_id_to_merge_into, actor=actor
        )
    except WordDoesNotExist as e:
        return create_response(
            success=False, message=e.message, status_code=e.status_code
        )
    except Exception as e:
        logger.debug(e, exc_info=True)
        return create_response(success=False, message=str(e), status_code=500)
    return create_response(message="xxx")


@bp.route("/<item_id>/lock", methods=["POST"])
@authorize(action=ResourceActionsEnum.merge_word, domain=ResourceDomainEnum.words)
def lock_or_unlock_word(item_id: str):
    """lock word for further edit, no more field version updates allowed
    only admin can do this, purpose is to stop new content being generated on mature stuff"""
    actor: User = request.environ["actor"]
    try:
        WordService.lock_or_unlock_word(item_id=item_id, actor=actor)
    except WordDoesNotExist as e:
        return create_response(
            success=False, message=e.message, status_code=e.status_code
        )
    except Exception as e:
        logger.debug(e, exc_info=True)
        return create_response(success=False, message=str(e), status_code=500)
    return create_response(message="xxx")
