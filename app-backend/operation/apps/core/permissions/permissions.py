from rest_framework.permissions import BasePermission


class IsSuperOrReadOnly(BasePermission):
    """Legacy: is_staff → escritura; cualquier autenticado → lectura."""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)


class IsAdminOrReadOnly(BasePermission):
    """Legacy: role code_name='admin' → escritura."""
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.roles.filter(code_name='admin').exists()
        )
