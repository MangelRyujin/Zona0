from dj_rest_auth.jwt_auth import get_refresh_view
from dj_rest_auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetConfirmView, PasswordResetView
from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView
from apps.users.api.views.point_view import OSP_PointView
from apps.users.api.views.verify_email_view import email_verification
from apps.users.api.views.image_view import ImageView


urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("password/change/", PasswordChangeView.as_view(), name="password_change"),
    path("password/reset/", PasswordResetView.as_view(), name="password_reset"),
    path("password/reset/confirm/", PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("token/refresh/", get_refresh_view().as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("email/verify/<str:token>/", email_verification, name="email_verify"),
    path("update/image-user/", ImageView.as_view(), name="update_image"),
    path("osp_points/",OSP_PointView, name="osp_points"),
    
]
