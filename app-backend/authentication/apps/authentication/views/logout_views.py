from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import BlacklistedToken, OutstandingToken

from apps.authentication.serializers.logout_serializers import LogoutSerializer

# pylint: disable=broad-exception-caught


class LogoutView(APIView):
    def post(self, request):
        """User logout

        Blacklist the refresh token of the current session
        ---
        Content/Type:
            application/json
        ---
        Header Parameters:
            Authorization: Bearer <user_token>
            x-api-key: <api key>
        ---
        Body Parameters:
            refresh_token: refresh token of the current session
        ---
        Status Codes:
            200 - Password updated successfully
            400 - An error creating the user
        """
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response("Ok", status=status.HTTP_200_OK)


class LogoutAllView(APIView):
    def post(self, request):
        """User logout

        Blacklist all refresh tokens of the user
        ---
        Content/Type:
            application/json
        ---
        Header Parameters:
            Authorization: Bearer <user_token>
            x-api-key: <api key>
        ---
        Status Codes:
            200 - Password updated successfully
            400 - An error creating the user
        """

        tokens = OutstandingToken.objects.filter(user_id=request.user.id)
        for token in tokens:
            BlacklistedToken.objects.get_or_create(token=token)

        return Response("Ok", status=status.HTTP_200_OK)
