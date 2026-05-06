from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from apps.authentication.models.permission import Permission
from apps.authentication.models.permission_group import PermissionGroup
from apps.authentication.models.role import Role

from apps.core.models.base_model import BaseModel


class User(BaseModel, AbstractUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    roles = models.ManyToManyField(Role, related_name="users", blank=True)
    image = models.ImageField(
        upload_to="user/",
        null=True,
        blank=True,
    )
    permission_groups = models.ManyToManyField(
        PermissionGroup, related_name="users", blank=True
    )

    # Usuario que creó este usuario (cadena de delegación jerárquica).
    created_by = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="created_users",
        verbose_name="Creado por",
    )

    class Meta:
        ordering = ["-created_at"]

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    @property
    def permissions(self):
        """
        Return user permissions
        """
        role_permissions_ids = self.roles.all().values_list(
            "permission_groups__permissions"
        )
        permission_group_permissions_ids = self.permission_groups.all().values_list(
            "permissions"
        )
        permission_ids = role_permissions_ids.union(permission_group_permissions_ids)
        return Permission.objects.filter(id__in=permission_ids)

    @property
    def grouped_permissions(self):
        """
        Return user permissions grouped by resource
        """
        permissions = self.permissions
        grouped_permissions = {}
        for permission in permissions:
            if permission.resource.code_name not in grouped_permissions:
                grouped_permissions[permission.resource.code_name] = []
            grouped_permissions[permission.resource.code_name].append(permission.action)
        return grouped_permissions
