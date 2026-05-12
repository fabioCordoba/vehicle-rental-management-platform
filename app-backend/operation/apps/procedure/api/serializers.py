from rest_framework import serializers
from apps.procedure.models import Procedure
from apps.procedure.services.vehicle_client import (
    get_vehicle,
    VehicleNotFound,
    VehicleServiceUnavailable,
)


class ProcedureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Procedure
        fields = [
            "id",
            "vehicle_id",
            "customer_id",
            "request_date",
            "start_date",
            "end_date",
            "status",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "is_active", "created_at", "updated_at"]


class ProcedureWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Procedure
        fields = [
            "vehicle_id",
            "customer_id",
            "request_date",
            "start_date",
            "end_date",
            "status",
        ]

    def validate(self, attrs):
        start_date = attrs.get("start_date")
        end_date = attrs.get("end_date")
        if start_date and end_date and end_date < start_date:
            raise serializers.ValidationError(
                {"end_date": "end_date must be after start_date."}
            )

        # Only validate vehicle availability on create, not on partial updates
        if self.instance is None:
            token = self.context.get("token", "")
            vehicle_id = attrs.get("vehicle_id")
            if vehicle_id:
                try:
                    vehicle = get_vehicle(str(vehicle_id), token)
                except VehicleNotFound:
                    raise serializers.ValidationError(
                        {"vehicle_id": "Vehicle not found."}
                    )
                except VehicleServiceUnavailable:
                    raise serializers.ValidationError(
                        {"vehicle_id": "Vehicle service is currently unavailable. Please try again later."}
                    )
                if not vehicle.get("is_available"):
                    raise serializers.ValidationError(
                        {"vehicle_id": "Vehicle is not available for rental."}
                    )

        return attrs
