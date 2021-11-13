from flask import Blueprint, request
from flask_pydantic import validate
from app.db.models.models import FieldVersion
from app.util.app_logging import get_logger
from app.casbin.decorator import authorize
from app.casbin.role_definition import ResourceDomainEnum, ResourceActionsEnum
from app.schemas.user import User
from app.schemas.field_version import FieldVersionCreate
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
def create_word(body: FieldVersionCreate):
    actor: User = request.environ["actor"]
    try:
        word = FieldVersion.create_field_version(item_create=body, actor=actor)
    except Exception as e:
        logger.debug(e, exc_info=True)
        return create_response(success=False, message=str(e), status_code=500)

    return create_response(response=word)
