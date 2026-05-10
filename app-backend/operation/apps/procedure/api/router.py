from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.procedure.api.views import ProcedureViewSet

router = DefaultRouter()
router.register(r"procedures", ProcedureViewSet, basename="procedure")

urlpatterns = [
    path("", include(router.urls)),
]
