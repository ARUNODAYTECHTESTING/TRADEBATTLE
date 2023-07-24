from rest_framework import serializers
from wallet import models as wallet_models

class DepositeWidthrawSerializer(serializers.ModelSerializer):
    is_transaction_in_rupees = serializers.BooleanField()
    is_transaction_in_coin = serializers.BooleanField()
    transaction_amount_or_coin = serializers.CharField(max_length=255)


    class Meta:
        model = wallet_models.Transaction
        fields = ["is_transaction_in_rupees","is_transaction_in_coin","transaction_amount_or_coin","credit_type"]

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