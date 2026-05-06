from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from rest_framework import serializers


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password_confirmation = serializers.CharField(required=True)

    def validate_old_password(self, old_password):
        user = self.context["request"].user

        if not user.check_password(old_password):
            raise serializers.ValidationError("The old password is incorrect.")

        return old_password

    def validate_new_password(self, new_password):
        user = self.context["request"].user
        errors = {}
        try:
            password_validation.validate_password(new_password, user)
        except ValidationError as e:
            errors["password"] = list(e.messages)
            raise serializers.ValidationError(errors)

        return new_password

    def validate(self, attrs):
        old_password = attrs["old_password"]
        new_password = attrs["new_password"]
        new_password_confirmation = attrs["new_password_confirmation"]

        if new_password != new_password_confirmation:
            raise serializers.ValidationError(
                {"new_password_confirmation": "Passwords do not match"}
            )

        if new_password == old_password:
            raise serializers.ValidationError(
                "The new password cannot be the same as the old password."
            )

        return attrs
