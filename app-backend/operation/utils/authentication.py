from rest_framework_simplejwt.authentication import JWTStatelessUserAuthentication
from rest_framework_simplejwt.models import TokenUser


class JWTUser(TokenUser):
    """TokenUser extended with the custom claims issued by the authentication microservice."""

    @property
    def email(self) -> str:
        return self.token.get("email", "")

    @property
    def is_staff(self) -> bool:
        return bool(self.token.get("is_staff", False))

    @property
    def role(self) -> str:
        return self.token.get("role", "")

    @property
    def hierarchy_level(self) -> str:
        return self.token.get("hierarchy_level", "")


class JWTAuthenticationFromAuth(JWTStatelessUserAuthentication):
    """Validates JWT tokens issued by the authentication microservice.

    Uses stateless validation — never queries the operation database.
    User identity and role are read directly from token claims.
    """

    def get_user(self, validated_token):
        return JWTUser(validated_token)
