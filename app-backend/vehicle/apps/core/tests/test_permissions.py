from unittest.mock import MagicMock

from apps.core.permissions.permissions import IsSuperOrReadOnly


def _req(user):
    req = MagicMock()
    req.user = user
    return req


def test_is_super_or_read_only_allows_staff():
    user = MagicMock(is_authenticated=True, is_staff=True)
    assert IsSuperOrReadOnly().has_permission(_req(user), MagicMock()) is True


def test_is_super_or_read_only_denies_non_staff():
    user = MagicMock(is_authenticated=True, is_staff=False)
    assert IsSuperOrReadOnly().has_permission(_req(user), MagicMock()) is False
