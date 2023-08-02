from django.urls import path
from .views import (
    ReferalView,
    TransactionView
)


urlpatterns = [
    path("referal/", ReferalView.as_view()),
    path("transaction/<credit_type>/", TransactionView.as_view()),
]