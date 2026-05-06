from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from apps.users.models.user import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        "username",
        "email",
        "get_roles",
        "is_active",
        "is_staff",
        "is_superuser",
    )
    list_filter = ("roles", "is_staff", "is_superuser", "is_active")

    def get_roles(self, obj):
        return ", ".join([role.title for role in obj.roles.all()])

    get_roles.short_description = "Roles"

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Personal info",
            {"fields": ("first_name", "last_name", "email", "image", "roles")},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "roles",
                    "image",
                    "password1",
                    "password2",
                ),
            },
        ),
    )

    search_fields = ("username", "email")
    ordering = ("username",)
