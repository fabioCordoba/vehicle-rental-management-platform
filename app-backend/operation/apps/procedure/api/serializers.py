from rest_framework import serializers
from apps.procedure.models import Procedure


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
        return attrs
