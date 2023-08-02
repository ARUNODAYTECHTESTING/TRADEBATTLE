from django.urls.conf import path

from .views import (
    load_payment_page,
    PaymentCallBackview
)

urlpatterns = [
    path("", load_payment_page),
    path("payment-callback/", PaymentCallBackview.as_view()),

]
