from rest_framework.routers import DefaultRouter

from apps.transport.api.views import TransportViewSet

router = DefaultRouter()
router.register(r"transports", TransportViewSet, basename="transport")

urlpatterns = router.urls
