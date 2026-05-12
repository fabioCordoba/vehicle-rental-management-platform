from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        errors = response.data
        if isinstance(errors, list):
            detail = errors
        elif isinstance(errors, dict):
            detail = {
                field: messages[0] if isinstance(messages, list) and len(messages) == 1 else messages
                for field, messages in errors.items()
            }
        else:
            detail = errors

        response.data = {
            "status_code": response.status_code,
            "detail": detail,
        }
        return response

    return Response(
        {"status_code": 500, "detail": "An unexpected error occurred."},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
