from dj_rest_auth.registration.views import RegisterView, ResendEmailVerificationView, VerifyEmailView
from django.urls import include, path, re_path
from django.views.generic import TemplateView

from .views import CustomConfirmEmailView

urlpatterns = [
    path("", include("dj_rest_auth.urls")),
    path(
        "registration/account-confirm-email/<str:key>/",
        CustomConfirmEmailView.as_view(),
        name="account_confirm_email",
    ),
    path("registration/", RegisterView.as_view(), name="rest_register"),
    re_path(r"registration/verify-email/?$", VerifyEmailView.as_view(), name="rest_verify_email"),
    re_path(r"registration/resend-email/?$", ResendEmailVerificationView.as_view(), name="rest_resend_email"),
    re_path(
        r"registration/account-email-verification-sent/?$",
        TemplateView.as_view(),
        name="account_email_verification_sent",
    ),
    path(
        "password/reset/confirm/<str:uidb64>/<str:token>/",
        TemplateView.as_view(template_name="authentication/password_reset_confirm.html"),
        name="password_reset_confirm",
    ),
]
