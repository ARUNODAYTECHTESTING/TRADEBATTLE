from django.contrib import admin
from news import models as news_models
# Register your models here.
admin.site.register(news_models.NewsCategory)
admin.site.register(news_models.News)
