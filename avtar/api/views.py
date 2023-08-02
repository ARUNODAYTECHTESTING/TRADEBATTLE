from rest_framework import generics
from avtar import models as avtar_models
from avtar.api import serializers as avtar_api_serializers
from rest_framework import permissions

class AvtarView(generics.ListCreateAPIView):
    permission_classes = [permissions.AllowAny]

    queryset = avtar_models.LevelAvtar.objects.all()
    serializer_class = avtar_api_serializers.AvtarSerilizer
   
class AvtarDetailsView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.AllowAny]

    queryset = avtar_models.LevelAvtar.objects.all()
    serializer_class = avtar_api_serializers.AvtarSerilizer

