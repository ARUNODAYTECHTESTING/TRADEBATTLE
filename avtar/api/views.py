from rest_framework import generics
from avtar import models as avtar_models
from avtar.api import serializers as avtar_api_serializers
from rest_framework import permissions

class AvtarView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    queryset = avtar_models.LevelAvtar.objects.all()
    serializer_class = avtar_api_serializers.AvtarSerilizer

    def get_queryset(self):
        exp_level_avtar = self.request.user.ex_level.levelavtar_set.all()
        return exp_level_avtar
      

   
class AvtarDetailsView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.AllowAny]

    queryset = avtar_models.LevelAvtar.objects.all()
    serializer_class = avtar_api_serializers.AvtarSerilizer

