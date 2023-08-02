from rest_framework import serializers
from avtar import models as avtar_models
from authentication import serializers as auth_serializers


class AvtarSerilizer(serializers.ModelSerializer):
    level = auth_serializers.ExperienceLevelSerializer(many=True)
    class Meta:
        model = avtar_models.LevelAvtar
        fields = ["id","name","image","level"]