from django.db import models

from apps.authentication.constants.permissions_constants import MethodOptions
from apps.core.models.base_model import BaseModel


class Permission(BaseModel):
    """
    Permission model

    Attributes:
        title (str): The title of the permission
        code_name (str): The code name of the permission
        resource (PermissionResource): The resource of the permission
        action (str): The action of the permission ie. create, analyze, etc.
        endpoint (str): The endpoint that the permission calls
        method (str): The HTTP method of the endpoint
        related_permissions (Permission): The related permissions
    """

    title = models.CharField(max_length=255, blank=True, null=True)
    code_name = models.CharField(max_length=255, unique=True)
    resource = models.ForeignKey(
        "PermissionResource", on_delete=models.PROTECT, related_name="permissions"
    )
    action = models.CharField(
        max_length=255,
        verbose_name="Action related to the permission ie. create, analyze, etc.",
    )
    endpoint = models.ForeignKey(
        "Endpoint",
        on_delete=models.CASCADE,
        verbose_name="Endpoint related to the permission",
    )
    method = models.CharField(
        max_length=255, choices=MethodOptions.choices, verbose_name="HTTP method"
    )
    related_permissions = models.ManyToManyField("self", blank=True, symmetrical=False)

    class Meta:
        verbose_name = "Permission"
        verbose_name_plural = "Permissions"
        unique_together = ["resource", "action"]

    def __str__(self):
        return self.code_name

    def save(self, *args, **kwargs):
        self.code_name = f"{self.resource.code_name}_{self.action}"
        self.full_clean()
        return super().save(*args, **kwargs)
