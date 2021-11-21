import casbin_sqlalchemy_adapter
import casbin
from app.config.app_config import conf
from app.casbin.role_definition import (
    ResourceRightsEnum,
    ResourceDomainEnum,
    resource_right_action_mapping,
)
import os
from app.casbin.seed import seed_or_get_admin_user


def create_casbin_enforcer():
    adapter = casbin_sqlalchemy_adapter.Adapter(conf.DATABASE_URI)
    casbin_enforcer = casbin.Enforcer("app/casbin/model.conf", adapter)
    # probably need to come from configurations?
    # now added a function here to
    print("creating casbin enforcer")

    def actions_mapping(
        action_from_request: str, resource_right_from_policy: str
    ) -> bool:
        """
        actions are get download patch share...
        resource_right are own / edit / view
        """
        if resource_right_from_policy in resource_right_action_mapping:
            if (
                action_from_request
                in resource_right_action_mapping[resource_right_from_policy]
            ):
                return True
        return False

    def objects_mapping(object_from_request: str, object_from_policy: str):
        """
        admin users will have * in obj in the admin role policy, so admin user can
        do things on any resource
        """
        if object_from_request.startswith(object_from_policy):
            # * means usper admin
            # startwith means specific dialect admin
            return True
        else:
            return object_from_request == object_from_policy

    casbin_enforcer.add_function("actions_mapping", actions_mapping)
    casbin_enforcer.add_function("objects_mapping", objects_mapping)
    # add admin role, only admin can create
    # well we cannot add policy this way because there are additional columns

    # well need to group all below stuff into seed...
    casbin_enforcer.add_policy(
        "admin-role-id", ResourceDomainEnum.words, ResourceRightsEnum.admin
    )
    casbin_enforcer.add_policy(
        "admin-role-id", ResourceDomainEnum.field_versions, ResourceRightsEnum.admin
    )
    casbin_enforcer.add_policy(
        "admin-role-id", ResourceDomainEnum.suggestions, ResourceRightsEnum.admin
    )
    admin_user_id = seed_or_get_admin_user()
    casbin_enforcer.add_grouping_policy(admin_user_id, "admin-role-id")
    # here, at first, there is no admin, admin only added via user management...
    # it is done via internal api call
    # but we can create specific service admin in the seed of the user management service
    return casbin_enforcer


casbin_enforcer = create_casbin_enforcer()
