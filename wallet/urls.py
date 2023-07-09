from django.urls import path
from .views import (
    ReferalView,
)


urlpatterns = [
    path("referal/", ReferalView.as_view())
]