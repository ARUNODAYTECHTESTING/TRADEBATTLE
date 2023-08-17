# authentication/serializers.py

from rest_framework import serializers
from authentication.models import ExperienceLevel, User
from shared.validator import phone_number_validator

class ExperienceLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExperienceLevel
        fields = "__all__"

class UserSendOtpAPISerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=15, required=True)
    forget = serializers.BooleanField(required=False)

class VerifyOtpViewSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=15, required=True)
    otp = serializers.CharField(max_length=10, required=True)

class ResendOtpViewSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=15, required=True)

class SetPasswordViewSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)

class LoginViewSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=15, required=True)
    password = serializers.CharField(required=True)

class UsernameViewSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50, required=True)

class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["image"]
