from rest_framework import serializers
from news import models as news_models

class NewsSerializer(serializers.ModelSerializer):

    class Meta:
        model = news_models.News
        fields = '__all__'