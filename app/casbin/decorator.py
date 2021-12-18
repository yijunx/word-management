from app.casbin.enforcer import casbin_enforcer
from app.casbin.role_definition import ResourceActionsEnum, ResourceDomainEnum
from app.casbin.resource_id_converter import get_resource_id_from_item_id
from flask import request
from app.db.models.models import CasbinRule
from app.exceptions.general_exceptions import NotAuthorized
from app.exceptions.user import AdminUserDoesNotExist
from app.util.process_request import get_user_info_from_request
from app.util.response_util import create_response
import app.repo.user as UserRepo
import app.repo.casbin as CasbinRepo
from app.db.database import get_db
from app.config.app_config import conf


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

            casbin_enforcer.load_policy()
            actor = get_user_info_from_request(request=request)
            with get_db() as db:
                UserRepo.get_or_create(db=db, actor=actor)

            role_ids = casbin_enforcer.get_implicit_roles_for_user(actor.id)
            if conf.WORD_ADMIN_ROLE_ID in role_ids:
                actor.is_word_admin = True

            if conf.FIELD_VERSION_ADMIN_ROLE_ID in role_ids:
                actor.is_field_version_admin = True

            if conf.SUGGESTION_ADMIN_ROLE_ID in role_ids:
                actor.is_suggestion_admin = True

            request.environ["actor"] = actor

            # now is_admin is a few meanings

            # request.environ["is_admin"] = is_admin

            # so now the we know if who is the requestor and if he is an admin here
            # then why casbin???, enforce what?
            # - enforce whether this guy can use admin endpoints
            # then this the only use now??
            # admin functions are
            # - all the activate and deactive
            # - merge word
            # - lock
            # then we also do not need the actions mappings..
            # well ummm.. this is it then?
            # even if with dynamic sharing casbin maybe not needed
            # But there is already actor and is admin
            # why do we need casbin?
            # admin info can be in the user table also
            # just a column of is_admin...
            # and let service raise the exception
            # if the user cannot use at all, or user cannot use if for certain item id
            # well its time to remove casbin?
            # whyyyyyyyyyy.. well if there are different domains
            # say word - admin, field_version - admin, suggestion - admin
            # this can also be solved via No-Casbin-design

            if require_casbin:
                # item_id: str = kwargs["item_id"]
                # resource_id = get_resource_id_from_item_id(
                #     item_id=item_id, domain=domain
                # )

                # need to time this...
                # i wasnt receiving any issues cos there was only one worker!!!
                # thus only one casbin enforcer
                # well this should be fast.. but it needs to read the whole db..

                if casbin_enforcer.enforce(actor.id, domain, action):
                    # enforce on if the ucare can perform certain thing in
                    # a domain, say only admin can deactive stuff in a certain domain

                    # some new idea on this..
                    #
                    print("casbin allows it..!")
                    # here i use actor because this is the initiator of the action

                    return func(*args, **kwargs)
                else:
                    e = NotAuthorized(
                        actor=actor, resource_id_or_domain=domain, action=action
                    )
                    return create_response(
                        status_code=e.status_code,
                        message=e.message,
                        success=False,
                    )
            else:
                return func(*args, **kwargs)

        # this is to prevent some view point!!
        wrapper_enforcer.__name__ = func.__name__
        return wrapper_enforcer

    return decorator
