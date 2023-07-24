from wallet import serializers as wallet_serializers

class WalletService:
    @staticmethod
    def validate_transaction_request(payload: dict, credit_type: int):
        if credit_type == 1:
            serializer = wallet_serializers.DepositeWidthrawSerializer(data = payload)
        if credit_type == 2:
            serializer = wallet_serializers.DepositeWidthrawSerializer(data = payload)
        if credit_type == 3:
            serializer = wallet_serializers.DepositeWidthrawSerializer(data = payload)
        if credit_type == 4:
            serializer = wallet_serializers.DepositeWidthrawSerializer(data = payload)
        if credit_type == 5:
            serializer = wallet_serializers.DepositeWidthrawSerializer(data = payload)
        if credit_type == 6:
            serializer = wallet_serializers.DepositeWidthrawSerializer(data = payload)
      
        if not serializer.is_valid():
            return 400,serializer.errors
        return 200 ," Deposite amount sucessfully"