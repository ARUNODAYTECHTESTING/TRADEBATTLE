# authentication/serializers.py

from rest_framework import serializers
from wallet import models as wallet_models
from django.db.models import Sum
from authentication.models import ExperienceLevel, User,LevelAvtar
from shared.validator import phone_number_validator
from authentication import models as auth_models
import pdb

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

    class Meta: 
        model = auth_models.User
        fields = ["image"]

class UserSerializer(serializers.ModelSerializer):
    ex_level = ExperienceLevelSerializer()
    total_coins = serializers.SerializerMethodField('get_total_coins')
    battle_played = serializers.SerializerMethodField('get_battle_played')
    
    class Meta: 
        model = auth_models.User
        fields = "__all__"
    
    def get_total_coins(self,obj):
        # pdb.set_trace() 
        amount=0.0
        if obj.wallet:
            amount = wallet_models.Transaction.objects.filter(wallet = obj.wallet,credit_type=1).aggregate(Sum('amount'))['amount__sum']
        return amount*10
    
    def get_battle_played(self,obj):
        return 105
class LoginViewSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=15, required=True)
    password = serializers.CharField(required=True)

class UsernameViewSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50, required=True)

class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["image"]



class AvtarSerilizer(serializers.ModelSerializer):
    level = ExperienceLevelSerializer(many=True)
    class Meta:
        model = LevelAvtar
        fields = ["id","name","image","level"]


