import logging

from rest_framework import serializers
from rest_framework_simplejwt import authentication
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken


class TokenRefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    class Meta:
        ref_name = "AppTokenRefresh"

    def validate(self, attrs):
        refresh = RefreshToken(attrs.get("refresh"))

        data = {"access": str(refresh.access_token)}

        if api_settings.ROTATE_REFRESH_TOKENS:
            if api_settings.BLACKLIST_AFTER_ROTATION:
                try:
                    refresh.blacklist()
                except AttributeError as e:
                    logging.error("Error while blacklisting refresh token: %s", e)

            refresh.set_jti()
            refresh.set_exp()

            data["refresh"] = str(refresh)
        validated_token = authentication.JWTAuthentication().get_validated_token(
            data.get("access")
        )
        authentication.JWTAuthentication().get_user(validated_token)
        return data
