from django.db import models
from apps.core.models.base_model import BaseModel

class Procedure(BaseModel):

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        ACTIVE = 'active', 'Active'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'

    vehicle_id = models.UUIDField()
    customer_id = models.UUIDField()
    request_date = models.DateField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
