import pytest
from unittest.mock import patch
from rest_framework.test import APIRequestFactory

from apps.users.api.views import UserViewSet

factory = APIRequestFactory()


def _viewset_for(user, action="list"):
    request = factory.get("/")
    request.user = user
    vs = UserViewSet()
    vs.request = request
    vs.action = action
    vs.kwargs = {}
    return vs


@pytest.mark.django_db
def test_platform_admin_queryset_includes_all_active_users(
    platform_admin_user, employee_user
):
    qs = _viewset_for(platform_admin_user).get_queryset()
    assert employee_user in qs


@pytest.mark.django_db
def test_org_admin_queryset_excludes_self(org_admin_user):
    qs = _viewset_for(org_admin_user).get_queryset()
    assert org_admin_user not in qs


@pytest.mark.django_db
def test_supervisor_queryset_contains_employees(supervisor_user, employee_user):
    qs = _viewset_for(supervisor_user).get_queryset()
    assert employee_user in qs


@pytest.mark.django_db
def test_destroy_sets_user_inactive(platform_admin_user, employee_user):
    request = factory.delete("/")
    request.user = platform_admin_user
    vs = UserViewSet()
    vs.request = request
    vs.action = "destroy"
    vs.kwargs = {}

    with patch.object(vs, "get_object", return_value=employee_user):
        vs.destroy(request)

    employee_user.refresh_from_db()
    assert employee_user.is_active is False
