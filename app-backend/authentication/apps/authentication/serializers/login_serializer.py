from typing import Any, cast, Dict
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.users.serializers.user_serializers import UserSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Claims embebidos en el JWT para validación stateless entre microservicios
        token["email"] = user.email
        token["is_staff"] = user.is_staff
        role = user.roles.first()
        if role:
            token["role"] = role.code_name
            token["hierarchy_level"] = role.hierarchy_level
        return token

    def validate(self, attrs) -> Dict[str, Any]:
        data = cast(Dict[str, Any], super().validate(attrs))
        data["user"] = UserSerializer(self.user).data
        return data
