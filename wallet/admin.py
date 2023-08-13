from django.contrib import admin
from wallet import models as wallet_models
# Register your models here.

admin.site.register(wallet_models.Wallet)
admin.site.register(wallet_models.Transaction)
