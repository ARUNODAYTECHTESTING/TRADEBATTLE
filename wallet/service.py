from wallet import serializers as wallet_serializers

class WalletService:
    @staticmethod
    def validate_transaction_request(payload: dict, credit_type: int):
        try:
            if credit_type == 1:
                serializer = wallet_serializers.DepositeWidthrawSerializer(data = payload)
            elif credit_type == 2:
                serializer = wallet_serializers.DepositeWidthrawSerializer(data = payload)
            elif credit_type == 3:
                serializer = wallet_serializers.BonusSerializer(data = payload)
            elif credit_type == 4:
                serializer = wallet_serializers.ContestSerializer(data = payload)
            elif credit_type == 5:
                serializer = wallet_serializers.WiningSerializer(data = payload)
            elif credit_type == 6:
                serializer = wallet_serializers.RefundSerializer(data = payload)
        except Exception as e:
            return 400, f"{e}"
        finally:
            if not serializer.is_valid():
                return 400,serializer.errors
        return 200 ," Deposite amount sucessfully"