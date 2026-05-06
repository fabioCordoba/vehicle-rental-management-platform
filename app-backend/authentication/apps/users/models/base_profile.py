from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q

from apps.authentication.models.role import HierarchyLevel
from apps.core.models.base_model import BaseModel
from apps.users.models.user import User


class BaseProfile(BaseModel):
    """
    Abstract base model for user profiles.

    Cada subclase debe declarar el atributo de clase EXPECTED_HIERARCHY_LEVEL
    con el nivel jerárquico requerido (HierarchyLevel.*).

    Ejemplo:
        class SupervisorProfile(BaseProfile):
            EXPECTED_HIERARCHY_LEVEL = HierarchyLevel.SUPERVISOR
    """

    # Subclases deben sobreescribir este atributo
    EXPECTED_HIERARCHY_LEVEL: str | None = None

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name="user_profile",
    )

    class Meta:
        abstract = True

    def clean(self):
        super().clean()
        self.clean_user_has_role()

    def clean_user_has_role(self):
        """
        Valida que el usuario tenga exactamente el rol esperado
        para este tipo de perfil (por hierarchy_level).
        """
        if not self.user_id:
            return

        expected = self.EXPECTED_HIERARCHY_LEVEL
        if expected is None:
            return

        user_roles = self.user.roles.all()

        # 1. Debe tener al menos un rol con el hierarchy_level esperado
        if not user_roles.filter(hierarchy_level=expected).exists():
            raise ValidationError({
                "user": (
                    f"El usuario {self.user.email} no tiene el rol requerido "
                    f"para este perfil (hierarchy_level='{expected}')."
                )
            })

        # 2. No debe tener roles de otro hierarchy_level (conflicto de jerarquía)
        conflicting = user_roles.filter(~Q(hierarchy_level=expected))
        if conflicting.exists():
            conflict_title = conflicting.first().title
            raise ValidationError({
                "user": (
                    f"El usuario {self.user.email} ya tiene el rol '{conflict_title}' "
                    f"(hierarchy_level='{conflicting.first().hierarchy_level}'), "
                    f"incompatible con este perfil."
                )
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
