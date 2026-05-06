from itertools import chain

from rest_framework.permissions import BasePermission


class RoleAuthorization(BasePermission):
    """
    Role authorization class

    This class is used to check if the user has permission to access the requested
    endpoint and method. Users must be active to use any element.
    """

    def validate_view_has_roles(self, view):
        role_permissions = getattr(view, "role_permissions", None)
        view_name = view.__class__.__name__

        if not role_permissions:
            raise ValueError(f"{view_name} must have role_permissions attribute")

        if not isinstance(role_permissions, dict):
            raise ValueError(f"{view_name} role_permissions must be a dictionary")

        if not all(isinstance(role, str) for role in role_permissions.keys()):
            raise ValueError(f"{view_name} role_permissions keys must be a string")

        for role, permissions in role_permissions.items():
            if not isinstance(permissions, list):
                raise ValueError(
                    f"{view_name} role_permissions permissions values must be a list"
                )

            for permission in permissions:
                if not isinstance(permission, str):
                    raise ValueError(
                        f"{view_name} role_permissions permissions elements "
                        f"must be strings"
                    )

    def has_permission(self, request, view):
        self.validate_view_has_roles(view)
        user = request.user
        user_roles_code_names = user.roles.values_list("code_name", flat=True)
        allowed_roles = view.role_permissions.keys()
        user_allowed_roles = set(allowed_roles).intersection(user_roles_code_names)
        if not user_allowed_roles:
            return False

        allowed_permissions = list(
            map(lambda x: view.role_permissions[x], user_allowed_roles)
        )
        allowed_permissions = list(chain.from_iterable(allowed_permissions))
        return view.action in allowed_permissions
