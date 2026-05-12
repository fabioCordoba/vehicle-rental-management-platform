from datetime import date

from rest_framework import serializers

from apps.transport.models import Transport


class TransportSerializer(serializers.ModelSerializer):
    condition_display = serializers.CharField(source="get_condition_display", read_only=True)

    class Meta:
        model = Transport
        fields = [
            "id",
            "make",
            "model",
            "year",
            "color",
            "license_plate",
            "condition",
            "condition_display",
            "passenger_capacity",
            "daily_rental_price",
            "is_available",
        ]


class TransportDetailSerializer(serializers.ModelSerializer):
    condition_display = serializers.CharField(source="get_condition_display", read_only=True)

    class Meta:
        model = Transport
        fields = [
            "id",
            "make",
            "model",
            "year",
            "color",
            "license_plate",
            "condition",
            "condition_display",
            "mileage",
            "passenger_capacity",
            "daily_rental_price",
            "is_available",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "is_active", "created_at", "updated_at"]


class TransportWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transport
        fields = [
            "make",
            "model",
            "year",
            "color",
            "license_plate",
            "condition",
            "mileage",
            "passenger_capacity",
            "daily_rental_price",
            "is_available",
        ]

    def validate_year(self, value):
        current_year = date.today().year
        if value < 1900 or value > current_year + 1:
            raise serializers.ValidationError(
                f"Year must be between 1900 and {current_year + 1}."
            )
        return value

    def validate_daily_rental_price(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Daily rental price must be greater than zero."
            )
        return value

    def validate_passenger_capacity(self, value):
        if value < 1:
            raise serializers.ValidationError(
                "Passenger capacity must be at least 1."
            )
        return value
