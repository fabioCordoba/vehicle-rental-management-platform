from rest_framework.permissions import IsAuthenticated
from apps.core.permissions.permissions import IsAdminOrReadOnly, IsSuperOrReadOnly
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from apps.users.serializers.user_serializers import (
    UserSerializer,
)
from rest_framework.response import Response

class CheckTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        refresh = RefreshToken.for_user(user)

        data = {
            "user": UserSerializer(user).data,
            "access": str(refresh.access_token),
            # "refresh": str(refresh),
        }
        return Response(data, status=200)