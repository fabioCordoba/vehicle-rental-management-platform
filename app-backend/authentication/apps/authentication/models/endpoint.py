from django.db import models

from apps.core.models.base_model import BaseModel


class Endpoint(BaseModel):
    """
    Endpoint model

    It is used to store the endpoints of the API and to relate them to the permissions

    Attributes:
        path (str): The path of the endpoint
    """

    path = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return str(self.path)
