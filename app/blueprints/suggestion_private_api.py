from flask import Blueprint, request
from flask_pydantic import validate
from app.exceptions.general_exceptions import NotAuthorized
from app.util.app_logging import get_logger
from app.casbin.decorator import authorize
from app.casbin.role_definition import ResourceDomainEnum, ResourceActionsEnum
from app.schemas.user import User
from app.schemas.suggestion import (
    SuggestionCreate,
    SuggestionPatch,
    SuggestionQuery,
)
import app.service.suggestion as SuggestionService
from app.util.response_util import create_response


# with this design, it is easier to make this into a separated service..
bp = Blueprint(
    name="suggestion_private_bp",
    import_name=__name__,
    url_prefix="/api/private/suggestions",
)

logger = get_logger(__name__)


@bp.route("", methods=["POST"])
@authorize(require_casbin=False)
@validate()
def create_suggestion(body: SuggestionCreate):
    actor: User = request.environ["actor"]
    try:
        r = SuggestionService.create_suggestion(item_create=body, actor=actor)
    except Exception as e:
        logger.debug(e, exc_info=True)
        return create_response(success=False, message=str(e), status_code=500)
    return create_response(response=r)


@bp.route("", methods=["GET"])
@authorize(require_casbin=False)
@validate()
def list_my_suggestions(query: SuggestionQuery):
    actor: User = request.environ["actor"]
    try:
        r = SuggestionService.list_suggestions(query=query, creator=actor)
    except Exception as e:
        logger.debug(e, exc_info=True)
        return create_response(success=False, message=str(e), status_code=500)
    return create_response(response=r)


@bp.route("/<item_id>", methods=["PATCH"])
@authorize(require_casbin=False)
@validate()
def update_my_suggestion(body: SuggestionPatch, item_id: str):
    actor: User = request.environ["actor"]
    try:
        r = SuggestionService.update_suggesion_content(
            item_patch=body, item_id=item_id, actor=actor
        )
    except NotAuthorized as e:
        return create_response(
            success=False, message=e.message, status_code=e.status_code
        )
    except Exception as e:
        logger.debug(e, exc_info=True)
        return create_response(success=False, message=str(e), status_code=500)
    return create_response(response=r)


@bp.route("/<item_id>/deactivate", methods=["POST"])
@authorize(
    action=ResourceActionsEnum.deactivate_suggestion,
    domain=ResourceDomainEnum.suggestions,
)
def activate_or_deactivate(item_id: str):
    """used for flipping the active flag, only admin user and suggestion owner can do this"""
    actor: User = request.environ["actor"]
    try:
        SuggestionService.activate_or_deactive_suggestion(item_id=item_id, actor=actor)
    except Exception as e:
        logger.debug(e, exc_info=True)
        return create_response(success=False, message=str(e), status_code=500)
    return create_response(message="xxx")
