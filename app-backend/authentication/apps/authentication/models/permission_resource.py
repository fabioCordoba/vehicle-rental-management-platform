from django.core.validators import RegexValidator
from django.db import models

from apps.core.models.base_model import BaseModel


class PermissionResource(BaseModel):
    """
    PermissionResource model

    It is used to store the resources of the API and to relate them to the permissions

    Attributes:
        title (str): The title of the permission resource (Display name)
        code_name (str): The code name of the permission resource (Unique identifier)
    """

    title = models.CharField(max_length=255)
    code_name = models.CharField(
        max_length=255,
        unique=True,
        validators=[
            RegexValidator(r"^[a-z]+(_[a-z]+)?$", message="Invalid code name format")
        ],
        help_text="Enter a code name using only letters. Optionally, separate words with "
        "a single underscore '_'. Only one underscore is allowed. "
        "ie.: 'code_name' or 'name'.",
    )

    class Meta:
        verbose_name = "Permission Resource"
        verbose_name_plural = "Permission Resources"

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        self.code_name = self.code_name.lower()
        self.full_clean()
        return super().save(*args, **kwargs)
