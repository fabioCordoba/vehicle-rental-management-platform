from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.authentication.serializers.change_password_serializer import (
    ChangePasswordSerializer,
)
from apps.users.models.user import User


class ChangePasswordViewSet(GenericViewSet):
    queryset = User.objects.filter(is_active=True)

    def get_serializer_class(self):
        return ChangePasswordSerializer

    def create(self, request):
        """Create new password to User
        ---
        this endpoint receives as parameters the, new password and the
        confirm new password.
        ---
        Content/Type:
            application/json
        ---
        Header Parameters:
            token: JWT access token of the user who is registered in the application
            Change-Pass-Data: base64 encrypted new password and confirmation password
            x-api-key: <api key>
        ---
        Body Parameters:
        {
            "old_password": "str",
            "new_password": "str",
            "new_password_confirmation": "str"
        }
        ---
        Response parameters:
            None
        ---
        Status codes:
            200 - Ok
            400 - Unable to perform the action
            401 - User is not authorized
            404 - Not found
        """

        user = request.user
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        new_password = serializer.validated_data.get("new_password")

        user.set_password(new_password)
        user.save()
        return Response({"message": "Password changed!"}, status=status.HTTP_200_OK)
