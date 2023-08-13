from authentication import models as auth_models
from rest_framework import serializers
from wallet import models as wallet_models
from django.db.models import Sum

class ExperienceLevelSerializer(serializers.ModelSerializer):

    class Meta: 
        model = auth_models.ExperienceLevel
        fields = "__all__" 

class UpdateProfileSerializer(serializers.ModelSerializer):

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
        amount = wallet_models.Transaction.objects.filter(wallet = obj.wallet,credit_type=1).aggregate(Sum('amount'))['amount__sum']
        return amount*10
    
    def get_battle_played(self,obj):
        return 105