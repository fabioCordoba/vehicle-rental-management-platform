from django.db import models

from apps.authentication.models.permission import Permission
from apps.core.models.base_model import BaseModel


class PermissionGroup(BaseModel):
    """
    Permission Group model

    It is used to group permissions together and assign them to roles or users

    Attributes:
        title (str): The title of the permission group
        code_name (str): The code name of the permission group
        permissions (Permission): The permissions that belong to the permission group
    """

    title = models.CharField(max_length=255, unique=True)
    code_name = models.CharField(max_length=255, unique=True)
    permissions = models.ManyToManyField(Permission, related_name="permission_groups")

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = "Permission Group"
        verbose_name_plural = "Permission Groups"
