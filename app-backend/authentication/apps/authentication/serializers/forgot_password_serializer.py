from rest_framework import serializers

from apps.users.models.user import User


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        attrs = super().validate(attrs)

        if not User.objects.filter(is_active=True, email=attrs["email"]).exists():
            raise serializers.ValidationError(
                {"status": "The user does not exist or is not available"}
            )

        return attrs
