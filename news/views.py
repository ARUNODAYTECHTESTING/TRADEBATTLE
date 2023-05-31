from django.shortcuts import render
from rest_framework import generics
from rest_framework import permissions
from news import models as news_models
from news import serializers as news_serializers
# Create your views here.


class NewView(generics.ListCreateAPIView):
    queryset = news_models.News.objects.all()
    serializer_class = news_serializers.NewsSerializer
    permission_classes = (permissions.AllowAny,)

class NewDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = news_models.News.objects.all()
    serializer_class = news_serializers.NewsSerializer
    permission_classes = (permissions.AllowAny,)
    lookup_field = 'id'






