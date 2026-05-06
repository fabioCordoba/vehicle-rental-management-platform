from django.urls import include, path
from rest_framework import routers

from apps.authentication.views.change_password_view import ChangePasswordViewSet
from apps.authentication.views.forgot_password_view import ForgotPasswordView
from apps.authentication.views.login_view import MyTokenObtainPairView
from apps.authentication.views.logout_views import LogoutAllView, LogoutView
from apps.authentication.views.refresh_views import TokenRefreshView
from apps.authentication.views.register_views import RegisterView
from apps.authentication.views.check_token_views import CheckTokenView
from apps.authentication.views.me_views import UserView
from apps.authentication.views.roles_view import AssignableRolesView
from apps.users.api.views import UserViewSet, UserSearchView, SendEmailTest

router = routers.DefaultRouter()
router.register(
    r"authentication/change_pwd", ChangePasswordViewSet, basename="change_pwd"
)
router.register(r"users", UserViewSet, basename="user")

urlpatterns = [
    path("authentication/register", RegisterView.as_view()),
    path(
        "authentication/login/",
        MyTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path("authentication/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("authentication/logout/", LogoutView.as_view(), name="token_logout"),
    path(
        "authentication/logout_all/", LogoutAllView.as_view(), name="token_logout_all"
    ),
    path(
        "authentication/forgot_password/",
        ForgotPasswordView.as_view(),
        name="forgot_password",
    ),
    path("authentication/check-token/", CheckTokenView.as_view(), name="check_token"),
    path("authentication/me", UserView.as_view()),
    path(
        "authentication/roles/", AssignableRolesView.as_view(), name="assignable_roles"
    ),
    path("users/search/", UserSearchView.as_view(), name="user-search"),
    # path("email/test", SendEmailTest.as_view()),
    path("", include(router.urls)),
]
