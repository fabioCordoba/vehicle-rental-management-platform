from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response
from apps.users.models import User
from apps.users.serializers.user_serializers import (
    UserSerializer,
    UserUpdateSerializer,
)
from rest_framework import status

class UserView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Obtain authenticated user information",
        operation_description="Returns the authenticated user information using the JWT token in the header.",
        responses={200: UserSerializer},
    )
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Update authenticated user data",
        operation_description="It receives the user's information and updates it. A JWT must be sent in the header.",
        request_body=UserUpdateSerializer,
        responses={
            200: openapi.Response("User successfully updated", UserUpdateSerializer),
            400: "Error in the request. Please check the data you have submitted.",
        },
    )
    def put(self, request):
        user = User.objects.get(id=request.user.id)
        serializer = UserUpdateSerializer(user, request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)