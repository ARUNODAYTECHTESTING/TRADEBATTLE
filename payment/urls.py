from django.urls.conf import path

from .views import (
    load_payment_page
)

urlpatterns = [
    path("", load_payment_page),

]
