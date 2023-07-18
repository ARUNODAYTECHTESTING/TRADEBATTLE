from rest_framework import serializers
from news import models as news_models


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = news_models.Category
        fields = ["id","name"]

class NewsSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = news_models.News
        fields = ["id","stock_news","category"]