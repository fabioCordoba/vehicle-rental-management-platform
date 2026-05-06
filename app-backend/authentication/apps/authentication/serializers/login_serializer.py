from typing import Any, cast, Dict
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.users.serializers.user_serializers import UserSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs) -> Dict[str, Any]:
        data = cast(Dict[str, Any], super().validate(attrs))
        user = self.user
        data["user"] = UserSerializer(user).data
        return data
