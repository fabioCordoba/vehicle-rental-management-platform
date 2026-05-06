from django.db import models

from apps.core.models.base_model import BaseModel


class HierarchyLevel(models.TextChoices):
    """
    Jerarquía de usuarios de la plataforma:

    PLATFORM_ADMIN — Superusuario técnico. Acceso total, gestiona cuentas de administradores.
    SUPERVISOR     — Visibilidad y control sobre los recursos de la plataforma.
    """

    PLATFORM_ADMIN = 'platform_admin', 'Platform Admin'
    SUPERVISOR = 'supervisor', 'Supervisor'


class Role(BaseModel):
    """
    Role model

    Attributes:
        title (str): The title of the role
        code_name (str): The code name of the role
        permission_groups (PermissionGroup): The permission groups that belong to the role
        hierarchy_level (HierarchyLevel): Position in the user hierarchy.
    """

    title = models.CharField(max_length=255)
    code_name = models.CharField(max_length=255, unique=True)
    permission_groups = models.ManyToManyField(
        "PermissionGroup", related_name="roles", blank=True
    )
    hierarchy_level = models.CharField(
        max_length=20,
        choices=HierarchyLevel.choices,
        default=HierarchyLevel.SUPERVISOR,
        db_index=True,
    )

    def __str__(self):
        return str(self.code_name)

    class Meta:
        verbose_name = "Role"
        verbose_name_plural = "Roles"
        ordering = ["-created_at", "title"]
