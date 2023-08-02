from rest_framework import serializers
from wallet import models as wallet_models

class DepositeWidthrawSerializer(serializers.ModelSerializer):
    is_transaction_in_rupees = serializers.BooleanField()
    is_transaction_in_coin = serializers.BooleanField()
    coin = serializers.CharField()
    rupees = serializers.CharField()


    class Meta:
        model = wallet_models.Transaction
        fields = ["is_transaction_in_rupees","is_transaction_in_coin","coin","rupees","credit_type"]

class BonusSerializer(serializers.ModelSerializer):

    class Meta:
        model = wallet_models.Transaction


class WiningSerializer(serializers.ModelSerializer):

    class Meta:
        model = wallet_models.Transaction
        
class ContestSerializer(serializers.ModelSerializer):

    class Meta:
        model = wallet_models.Transaction
        
class RefundSerializer(serializers.ModelSerializer):

    class Meta:
        model = wallet_models.Transaction