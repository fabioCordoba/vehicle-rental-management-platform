import uuid

import pytest

from apps.authentication.models.role import Role, HierarchyLevel


@pytest.mark.django_db
def test_disable_sets_is_active_false(db):
    role = Role.objects.create(
        title="Temp",
        code_name="temp_disable_test",
        hierarchy_level=HierarchyLevel.SUPERVISOR,
    )
    role.disable()
    role.refresh_from_db()
    assert role.is_active is False


@pytest.mark.django_db
def test_id_is_uuid(db):
    role = Role.objects.create(
        title="Temp",
        code_name="temp_uuid_test",
        hierarchy_level=HierarchyLevel.SUPERVISOR,
    )
    assert isinstance(role.id, uuid.UUID)
