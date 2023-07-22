from authentication import models as auth_models
from rest_framework import serializers

class ExperienceLevelSerializer(serializers.ModelSerializer):

    class Meta: 
        model = auth_models.ExperienceLevel
        fields = "__all__" 

class UpdateProfileSerializer(serializers.ModelSerializer):

    class Meta: 
        model = auth_models.User
        fields = ["image"]