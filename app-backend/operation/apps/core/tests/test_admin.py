from unittest.mock import MagicMock

from django.contrib import admin

from apps.core.admin import ModelOnlyShowSuperAdmin, ModelOnlyEditableSuperAdmin


def _req(is_superuser=False, is_staff=False):
    req = MagicMock()
    req.user.is_superuser = is_superuser
    req.user.is_staff = is_staff
    return req


def test_only_show_super_admin_grants_superuser():
    model_admin = ModelOnlyShowSuperAdmin(model=MagicMock(), admin_site=admin.site)
    assert model_admin.has_module_permission(_req(is_superuser=True)) is True


def test_only_show_super_admin_denies_regular_staff():
    model_admin = ModelOnlyShowSuperAdmin(model=MagicMock(), admin_site=admin.site)
    assert model_admin.has_module_permission(_req(is_staff=True)) is False


def test_only_editable_super_admin_staff_cannot_change():
    model_admin = ModelOnlyEditableSuperAdmin(model=MagicMock(), admin_site=admin.site)
    assert model_admin.has_change_permission(_req(is_staff=True)) is False
