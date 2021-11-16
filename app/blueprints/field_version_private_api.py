from flask import Blueprint, request
from flask_pydantic import validate
from app.exceptions.vote import VoteAlreadyExist, VoteDoesNotExist
from app.schemas.suggestion import SuggestionAccept
from app.schemas.vote import VoteCreate
from app.util.app_logging import get_logger
from app.casbin.decorator import authorize
from app.casbin.role_definition import ResourceDomainEnum, ResourceActionsEnum
from app.schemas.user import User
from app.schemas.field_version import (
    FieldVersionCreate,
    FieldVersionPatch,
    FieldVersionQuery,
)
import app.service.field_version as FieldVersionService
from app.util.response_util import create_response


# with this design, it is easier to make this into a separated service..
bp = Blueprint(
    name="field_version_private_bp",
    import_name=__name__,
    url_prefix="/private_api/field_versions",
)

logger = get_logger(__name__)


@bp.route("", methods=["POST"])
@authorize(require_casbin=False)
@validate()
def create_field_version(body: FieldVersionCreate):
    actor: User = request.environ["actor"]
    try:
        word = FieldVersionService.create_field_version(item_create=body, actor=actor)
    except Exception as e:
        logger.debug(e, exc_info=True)
        return create_response(success=False, message=str(e), status_code=500)
    return create_response(response=word)


@bp.route("", methods=["GET"])
@authorize(require_casbin=False)
@validate()
def list_my_field_verions(query: FieldVersionQuery):
    actor: User = request.environ["actor"]
    try:
        field_versions_with_paging = FieldVersionService.list_field_version(
            query=query, creator=actor
        )
    except Exception as e:
        logger.debug(e, exc_info=True)
        return create_response(success=False, message=str(e), status_code=500)
    return create_response(response=field_versions_with_paging)


@bp.route("/<item_id>", methods=["PATCH"])
@authorize(
    action=ResourceActionsEnum.update_field_version_content,
    domain=ResourceDomainEnum.field_versions,
)
@validate()
def update_my_field_version(body: FieldVersionPatch, item_id: str):
    actor: User = request.environ["actor"]
    try:
        field_version = FieldVersionService.update_field_version_content(
            item_patch=body, item_id=item_id, actor=actor
        )
    except Exception as e:
        logger.debug(e, exc_info=True)
        return create_response(success=False, message=str(e), status_code=500)
    return create_response(response=field_version)


@bp.route("/<item_id>/accept_suggestion", methods=["POST"])
@authorize(
    action=ResourceActionsEnum.accept_or_reject_suggestion,
    domain=ResourceDomainEnum.field_versions,
)
@validate()
def accept_suggestion_to_my_field_version(body: SuggestionAccept, item_id: str):
    actor: User = request.environ["actor"]
    try:
        FieldVersionService.accept_suggestion_to_my_version(
            item_id=item_id, suggestion_id=body.suggestion_id, actor=actor
        )
    except Exception as e:
        logger.debug(e, exc_info=True)
        return create_response(success=False, message=str(e), status_code=500)
    return create_response(message="suggestion approved..")


@bp.route("/<item_id>/vote", methods=["POST"])
@authorize(require_casbin=False)
@validate()
def vote_a_field_version(body: VoteCreate, item_id: str):
    actor: User = request.environ["actor"]
    try:
        FieldVersionService.vote(item_id=item_id, vote_create=body, actor=actor)
    except VoteAlreadyExist as e:
        return create_response(success=False, message=str(e), status_code=e.http_code)
    except Exception as e:
        logger.debug(e, exc_info=True)
        return create_response(success=False, message=str(e), status_code=500)
    return create_response(message="voted!")


@bp.route("/<item_id>/unvote", methods=["POST"])
@authorize(require_casbin=False)
def unvote_a_field_version(item_id: str):
    actor: User = request.environ["actor"]
    try:
        FieldVersionService.unvote(item_id=item_id, actor=actor)
    except VoteDoesNotExist as e:
        return create_response(success=False, message=str(e), status_code=e.http_code)
    except Exception as e:
        logger.debug(e, exc_info=True)
        return create_response(success=False, message=str(e), status_code=500)
    return create_response(message="unvoted!")


@bp.route("/<item_id>/deactivate", methods=["POST"])
@authorize(
    action=ResourceActionsEnum.deactivate_field_version,
    domain=ResourceDomainEnum.field_versions,
)
def activate_or_deactivate(item_id: str):
    """used for flipping the active flag, only admin user can do this"""
    actor: User = request.environ["actor"]
    try:
        pass
    # word = WordService.update_word_title(body=body, actor=actor, item_id=item_id)
    except Exception as e:
        logger.debug(e, exc_info=True)
        return create_response(success=False, message=str(e), status_code=500)
    return create_response(message="xxx")
