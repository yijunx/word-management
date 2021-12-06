from flask.testing import FlaskClient
from app.schemas.user import User
from app.schemas.casbin_rule import CasbinRule, CasbinRuleWithPaging


def test_add_admin_user(client_without_user: FlaskClient, admin_user_to_add: User):
    r = client_without_user.post(
        f"/api/internal/admin_users", json=admin_user_to_add.dict()
    )
    assert r.status_code == 200


def test_list_admin_users(client_without_user: FlaskClient, admin_user_to_add: User):
    r = client_without_user.get(
        f"/api/internal/admin_users",
    )
    rule_with_paging = CasbinRuleWithPaging(**r.get_json()["response"])
    assert admin_user_to_add.id in [x.v0 for x in rule_with_paging.data]


def test_get_admin_user(client_without_user: FlaskClient, admin_user_to_add: User):
    r = client_without_user.get(
        f"/api/internal/admin_users/{admin_user_to_add.id}",
    )
    casbin_rule = CasbinRule(**r.get_json()["response"])
    assert admin_user_to_add.id == casbin_rule.v0


def test_remove_admin_user(client_without_user: FlaskClient, admin_user_to_add: User):
    r = client_without_user.delete(
        f"/api/internal/admin_users/{admin_user_to_add.id}",
    )
    assert r.status_code == 200
    r = client_without_user.get(
        f"/api/internal/admin_users",
    )
    rule_with_paging = CasbinRuleWithPaging(**r.get_json()["response"])
    assert admin_user_to_add.id not in [x.v0 for x in rule_with_paging.data]
