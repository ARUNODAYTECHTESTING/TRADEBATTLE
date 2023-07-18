from django.contrib import admin
from news import models as news_models
# Register your models here.
admin.site.register(news_models.Category)
admin.site.register(news_models.News)
