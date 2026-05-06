import pytest
from django.contrib import admin

from apps.users.admin import UserAdmin
from apps.users.models import User


@pytest.mark.django_db
def test_get_roles_returns_role_title(employee_user, role_employee):
    user_admin = UserAdmin(model=User, admin_site=admin.site)
    assert user_admin.get_roles(employee_user) == role_employee.title


@pytest.mark.django_db
def test_get_roles_returns_empty_string_when_user_has_no_roles(db):
    user = User.objects.create_user(
        email="noroles@test.com",
        username="noroles",
        password="TestPass1234!",
    )
    user_admin = UserAdmin(model=User, admin_site=admin.site)
    assert user_admin.get_roles(user) == ""
