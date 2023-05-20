from django.urls.conf import path

from .views import (
    ResendOtpVIew,
    UserSendOtpAPI,
    VerifyOtpView,
    LoginView,
    SetPasswordView,
    LoginView
)

urlpatterns = [
    path("verify-otp/", VerifyOtpView.as_view()),
    path("send-otp/", UserSendOtpAPI.as_view()),
    path("resend-otp/", ResendOtpVIew.as_view()),
    path("login/", LoginView.as_view()),
    path("set-password/", SetPasswordView.as_view()),
    path("login/", LoginView.as_view()),
]