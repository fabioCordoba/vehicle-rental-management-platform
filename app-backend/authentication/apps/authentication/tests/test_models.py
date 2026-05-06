import pytest

from apps.authentication.models.role import HierarchyLevel, Role
from apps.authentication.models.permission_resource import PermissionResource


@pytest.mark.django_db
def test_role_str_returns_code_name(db):
    role = Role.objects.create(
        title="Test Role",
        code_name="test_str_role",
        hierarchy_level=HierarchyLevel.SUPERVISOR,
    )
    assert str(role) == "test_str_role"


@pytest.mark.django_db
def test_role_default_hierarchy_level_is_supervisor(db):
    role = Role.objects.create(title="Supervisor Role", code_name="default_level_role")
    assert role.hierarchy_level == HierarchyLevel.SUPERVISOR


@pytest.mark.django_db
def test_permission_resource_code_name_lowercased_on_save(db):
    resource = PermissionResource(title="Animals", code_name="ANIMALS")
    resource.save()
    assert resource.code_name == "animals"
