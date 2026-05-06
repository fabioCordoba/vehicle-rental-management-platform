import json

from drf_yasg.openapi import Schema
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.views import Response

# from alternova_351conversion.task_handler import handle_task
from apps.authentication.methods.password_generator_methods import generate_password
from apps.authentication.serializers.forgot_password_serializer import (
    ForgotPasswordSerializer,
)
from apps.users.models.user import User


class ForgotPasswordView(GenericAPIView):
    """
    Forgot password flow
        ---
        this endpoint is use to generate a new
        password for the user and send it to email.
        ---
        Content/Type:
            application/json
        ---
        Header Parameters:
            x-api-key: <api key>
        ---
        Body Parameters:
        {
            "email": "example@example.com",
        }
        ---
        Response parameters:
        {
            "datail": "New password sent to example@example.com",
        }
        ---
        Status codes:
            200 - Ok
            400 - Unable to perform the action
    """

    serializer_class = ForgotPasswordSerializer
    permission_classes = [
        AllowAny,
    ]

    @swagger_auto_schema(
        operation_description="This operation allows users to "
        "generate a new password and receive it via email. "
        "Users should provide their email "
        "in the request body with a valid format.",
        responses={200: "Ok", 400: "Bad Request", 401: "Unauthorized"},
        request_body=Schema(
            type="object",
            properties={
                "email": Schema(type="string"),
            },
            required=["email"],
        ),
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = User.objects.get(email=serializer.validated_data["email"])

        password = generate_password()
        print(password)

        user.set_password(password)
        user.save()

        # handle_task(
        #     module="apps.common.methods.send_email",
        #     function="send_email",
        #     queue="celery",
        #     subject="Backend Template Password Recovery",
        #     template="backend_template_forgot_password",
        #     recipients=[user.email],
        #     email_data=json.dumps({"new_password": password, "email": user.email}),
        # )

        return Response("Ok", status.HTTP_200_OK)
