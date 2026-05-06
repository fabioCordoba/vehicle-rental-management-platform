import pytest
from rest_framework.test import APIRequestFactory

from apps.authentication.views.roles_view import AssignableRolesView

factory = APIRequestFactory()


@pytest.mark.django_db
def test_assignable_roles_platform_admin_sees_org_admin_role(
    platform_admin_user, role_org_admin
):
    request = factory.get("/")
    request.user = platform_admin_user

    view = AssignableRolesView()
    response = view.get(request)

    returned_codes = [r["code_name"] for r in response.data]
    assert role_org_admin.code_name in returned_codes


@pytest.mark.django_db
def test_assignable_roles_non_staff_excludes_org_admin_role(
    org_admin_user, role_org_admin, role_supervisor
):
    request = factory.get("/")
    request.user = org_admin_user

    view = AssignableRolesView()
    response = view.get(request)

    returned_codes = [r["code_name"] for r in response.data]
    assert role_org_admin.code_name not in returned_codes
