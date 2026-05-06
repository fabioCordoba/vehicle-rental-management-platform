from authentication import settings
from django.db import models


class MethodOptions(models.TextChoices):
    GET = "GET", "GET"
    POST = "POST", "POST"
    PUT = "PUT", "PUT"
    PATCH = "PATCH", "PATCH"
    DELETE = "DELETE", "DELETE"
    HEAD = "HEAD", "HEAD"
    OPTIONS = "OPTIONS", "OPTIONS"
    TRACE = "TRACE", "TRACE"
    CONNECT = "CONNECT", "CONNECT"


IGNORED_ENDPOINTS = [
    f"{settings.ADMIN_URL}",
    f"{settings.ADMIN_HONEYPOT_URL}",
]
