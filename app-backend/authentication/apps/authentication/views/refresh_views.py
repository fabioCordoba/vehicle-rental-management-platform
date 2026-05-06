from rest_framework_simplejwt.views import TokenViewBase

from apps.authentication.serializers.refresh_serializer import TokenRefreshSerializer


class TokenRefreshView(TokenViewBase):
    """
    Takes a refresh type JSON web token and returns an access type JSON web
    token if the refresh token is valid.
    """

    class Meta:
        ref_name = "SimpleJWTTokenRefresh"

    serializer_class = TokenRefreshSerializer
