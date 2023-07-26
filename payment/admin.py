from django.contrib import admin
from payment import models as payment_models
# Register your models here.

admin.site.register(payment_models.Order)