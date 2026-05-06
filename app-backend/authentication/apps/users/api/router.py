from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView
from apps.users.api.views import (
    SendEmailTest,
    UserSearchView,
    UserViewSet,
)
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"users", UserViewSet, basename="user")

urlpatterns = [
    path("email/test", SendEmailTest.as_view()),
    path("users/search/", UserSearchView.as_view(), name="user-search"),
    path("", include(router.urls)),
]
