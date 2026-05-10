from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsPlatformAdmin(BasePermission):
    """Write access only for platform_admin users (is_staff=True in JWT)."""

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_staff
        )


class IsSupervisorOrAbove(BasePermission):
    """Write access for supervisor and platform_admin hierarchy levels."""

    _allowed = {"supervisor", "platform_admin"}

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.hierarchy_level in self._allowed
        )


# ── Backwards-compatible aliases ──────────────────────────────────────────────

class IsSuperOrReadOnly(IsPlatformAdmin):
    """Alias kept for backwards compatibility. Prefer IsPlatformAdmin."""


class IsAdminOrReadOnly(IsSupervisorOrAbove):
    """Alias kept for backwards compatibility. Prefer IsSupervisorOrAbove."""
