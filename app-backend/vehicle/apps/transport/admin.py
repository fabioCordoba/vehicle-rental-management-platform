from django.contrib import admin

from apps.transport.models import Transport


@admin.register(Transport)
class TransportAdmin(admin.ModelAdmin):
    list_display = [
        "make",
        "model",
        "year",
        "license_plate",
        "condition",
        "mileage",
        "passenger_capacity",
        "daily_rental_price",
        "is_available",
        "is_active",
        "created_at",
    ]
    list_filter = ["condition", "is_available", "is_active", "make"]
    search_fields = ["make", "model", "license_plate", "color"]
    readonly_fields = ["id", "created_at", "updated_at"]
    ordering = ["-created_at"]
    list_per_page = 25
