from app.casbin.enforcer import casbin_enforcer
from app.casbin.role_definition import ResourceActionsEnum, ResourceDomainEnum
from app.casbin.resource_id_converter import get_resource_id_from_item_id
from flask import request
from app.util.process_request import get_user_info_from_request
from app.util.response_util import create_response


def authorize(action: ResourceActionsEnum, domain: ResourceDomainEnum):
    def decorator(func):
        def wrapper_enforcer(*args, **kwargs):
            actor = get_user_info_from_request(request=request)

            item_id: str = kwargs["item_id"]
            resource_id = get_resource_id_from_item_id(item_id=item_id, domain=domain)

            if casbin_enforcer.enforce(actor.id, resource_id, action):
                print("casbin allows it..!")
                # here i use actor because this is the initiator of the action
                request.environ["actor"] = actor
                return func(*args, **kwargs)
            else:
                return create_response(
                    status_code=403,
                    message=f"User {actor.id} has no right to {action} resource {resource_id}",
                    success=False,
                )

        # this is to prevent some view point!!
        wrapper_enforcer.__name__ = func.__name__
        return wrapper_enforcer

    return decorator
