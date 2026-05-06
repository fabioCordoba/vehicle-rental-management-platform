from rest_framework import serializers
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True)

    def remove_refresh_token(self, refresh_token):
        """
        Remove the refresh token from the database
        """
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return token
        except TokenError as e:
            raise serializers.ValidationError(e) from e

    def validate(self, attrs):
        """
        Validate the serializer
        """
        self.remove_refresh_token(attrs["refresh_token"])
        return attrs
