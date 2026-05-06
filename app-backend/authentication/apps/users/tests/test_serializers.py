import pytest

from apps.users.serializers.user_serializers import (
    UserCreateByOrgAdminSerializer,
    UserSerializer,
)


@pytest.mark.django_db
def test_user_serializer_returns_hierarchy_level(employee_user, role_employee):
    data = UserSerializer(employee_user).data
    assert data["hierarchy_level"] == role_employee.hierarchy_level


@pytest.mark.django_db
def test_user_serializer_hierarchy_level_is_none_without_roles(db):
    from apps.users.models import User

    user = User.objects.create_user(
        email="noroles3@test.com",
        username="noroles3",
        password="TestPass1234!",
    )
    data = UserSerializer(user).data
    assert data["hierarchy_level"] is None


@pytest.mark.django_db
def test_create_by_org_admin_invalid_when_passwords_mismatch(role_employee):
    serializer = UserCreateByOrgAdminSerializer(
        data={
            "email": "new@test.com",
            "username": "newuser",
            "password": "TestPass1234!",
            "password_confirmation": "OtherPass!",
            "role": str(role_employee.id),
        }
    )
    assert serializer.is_valid() is False
