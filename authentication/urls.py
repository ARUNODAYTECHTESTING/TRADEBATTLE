from django.urls.conf import path

from .views import (
    ResendOtpVIew,
    UserSendOtpAPI,
    VerifyOtpView,
    LoginView,
    SetPasswordView,
    LoginView,
    UsernameView,
    UpdateProfile,
    ProfileView
    
)

urlpatterns = [
    path("verify-otp/", VerifyOtpView.as_view()),
    path("send-otp/", UserSendOtpAPI.as_view()),
    path("resend-otp/", ResendOtpVIew.as_view()),
    path("login/", LoginView.as_view()),
    path("set-password/", SetPasswordView.as_view()),
    path("login/", LoginView.as_view()),
    path("username/", UsernameView.as_view()),
    path("profile/", ProfileView.as_view()),
    path('update-profile/',UpdateProfile.as_view())
    
]