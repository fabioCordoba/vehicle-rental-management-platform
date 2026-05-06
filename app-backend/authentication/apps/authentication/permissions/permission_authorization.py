from drf_yasg.generators import EndpointEnumerator
from rest_framework.permissions import BasePermission


class PermissionAuthorization(BasePermission):
    """
    Permission authorization class

    This class is used to check if the user has permission to access the requested
    endpoint and method. Users must be active to use any element.
    """

    def has_permission(self, request, view):
        user = request.user
        route = rf"{view.request.resolver_match.route}"
        route = EndpointEnumerator().get_path_from_regex(route)
        return (
            user.permissions.filter(
                endpoint__path=route,
                method=view.request.method,
                is_active=True,
            ).exists()
            and user.is_active
        )
