from rest_framework import serializers
from news import models as news_models


class NewsCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = news_models.NewsCategory
        fields = ["id","name"]

class NewsSerializer(serializers.ModelSerializer):
    category = NewsCategorySerializer()
    class Meta:
        model = news_models.News
        fields = ["id","stock_news","category"]