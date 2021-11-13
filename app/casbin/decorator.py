from app.casbin.enforcer import casbin_enforcer
from app.casbin.role_definition import ResourceActionsEnum, ResourceDomainEnum
from app.casbin.resource_id_converter import get_resource_id_from_item_id
from flask import request
from app.util.process_request import get_user_info_from_request
from app.util.response_util import create_response
import app.repo.user as UserRepo
from app.db.database import get_db


def authorize(
    action: ResourceActionsEnum = None,
    domain: ResourceDomainEnum = None,
    require_casbin: bool = True,
):
    """
    for those action requires identity (authentication),
    nginx will authenticate first then pass here.
    so, user without login will not pass authenticate

    the decorated function must have "item_id" as a keyward arg
    """

    def decorator(func):
        def wrapper_enforcer(*args, **kwargs):
            actor = get_user_info_from_request(request=request)

            with get_db() as db:
                UserRepo.get_or_create(db=db, actor=actor)

            request.environ["actor"] = actor
            if require_casbin:
                item_id: str = kwargs["item_id"]
                resource_id = get_resource_id_from_item_id(
                    item_id=item_id, domain=domain
                )
                if casbin_enforcer.enforce(actor.id, resource_id, action):
                    print("casbin allows it..!")
                    # here i use actor because this is the initiator of the action

                    return func(*args, **kwargs)
                else:
                    return create_response(
                        status_code=403,
                        message=f"User {actor.id} has no right to {action} resource {resource_id}",
                        success=False,
                    )
            else:
                return func(*args, **kwargs)

        # this is to prevent some view point!!
        wrapper_enforcer.__name__ = func.__name__
        return wrapper_enforcer

    return decorator
