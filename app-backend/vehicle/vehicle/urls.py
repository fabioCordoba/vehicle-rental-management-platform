from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from apps.transport.api.router import urlpatterns as transport_urlpatterns


def health(request):
    return JsonResponse({"status": "ok", "service": "vehicle"})


urlpatterns = [
    path("health/", health),
    path("admin/", admin.site.urls),
    path("api/", include(transport_urlpatterns)),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]
