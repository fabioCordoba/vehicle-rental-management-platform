from django.db import models
from apps.core.models.base_model import BaseModel


class Transport(BaseModel):
    class Condition(models.TextChoices):
        EXCELLENT = "excellent", "Excellent"
        GOOD = "good", "Good"
        FAIR = "fair", "Fair"
        POOR = "poor", "Poor"

    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.PositiveSmallIntegerField()
    color = models.CharField(max_length=50)
    license_plate = models.CharField(max_length=20, unique=True)
    condition = models.CharField(max_length=20, choices=Condition.choices, default=Condition.GOOD)
    mileage = models.PositiveIntegerField(default=0)
    passenger_capacity = models.PositiveSmallIntegerField()
    daily_rental_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.year} {self.make} {self.model} ({self.license_plate})"