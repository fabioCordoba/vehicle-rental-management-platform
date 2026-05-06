from django.contrib import admin
from django.shortcuts import redirect
from rest_framework_simplejwt.tokens import OutstandingToken

from apps.authentication.fixtures.endpoint_fixtures import (
    update_endpoints_and_permissions,
)

from apps.authentication.models.endpoint import Endpoint
from apps.authentication.models.permission import Permission
from apps.authentication.models.permission_group import PermissionGroup
from apps.authentication.models.permission_resource import PermissionResource
from apps.authentication.models.role import Role
from apps.core.admin import (
    ModelOnlyEditableSuperAdmin,
)

admin.site.unregister(OutstandingToken)

@admin.register(Endpoint)
class EndpointAdmin(ModelOnlyEditableSuperAdmin):
    list_display = ("path",)
    search_fields = ("path",)
    change_list_template = "admin/endpoint_change_list.html"

    def changelist_view(self, request, extra_context=None):  # pragma: no cover
        if request.GET.get("update_endpoints"):
            update_endpoints_and_permissions()
            return redirect("admin:authentication_endpoint_changelist")

        return super().changelist_view(request, extra_context)
    
@admin.register(OutstandingToken)
class OutstandingTokenAdmin(ModelOnlyEditableSuperAdmin):
    model = OutstandingToken
    list_display = ("id", "jti", "user", "created_at", "expires_at")

@admin.register(Permission)
class PermissionAdmin(ModelOnlyEditableSuperAdmin):
    list_display = ("title", "code_name", "action", "endpoint")
    list_filter = ("code_name", "action", "endpoint__path")
    search_fields = ("code_name", "action", "endpoint__path")
    readonly_fields = ("code_name",)


@admin.register(PermissionGroup)
class PermissionGroupAdmin(ModelOnlyEditableSuperAdmin):
    list_display = ("title", "code_name")
    search_fields = ("title", "code_name")


@admin.register(PermissionResource)
class PermissionResourceAdmin(ModelOnlyEditableSuperAdmin):
    list_display = ("title", "code_name")
    search_fields = ("title", "code_name")


@admin.register(Role)
class RoleAdmin(ModelOnlyEditableSuperAdmin):
    list_display = ("title", "code_name")
    search_fields = ("title", "code_name")
    filter_horizontal = ("permission_groups",)
