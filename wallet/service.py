from wallet import serializers as wallet_serializers
from shared import utils
from payment import service as payment_service
class WalletService:
    @staticmethod
    def validate_transaction_request(request,payload: dict, credit_type: int):
        try:
            if credit_type == 1:
                serializer = wallet_serializers.DepositeWidthrawSerializer(data = payload)
                if not serializer.is_valid():
                    return 400, serializer.errors
                elif serializer.data['is_transaction_in_coin'] in ["true",True]:
                    amount = utils.Conversion.rupees_to_coin(serializer.data['coin'])
                    payment_service.create_order({'amount': amount, 'currency':'INR','receipt':request.user.mobile,'message':f"Deposit amount using coin: {serializer.data['coin']} -> {amount}"})

                else:
                    coin = utils.Conversion.rupees_to_coin(serializer.data['rupees'])
                    amount = serializer.data['rupees']
                    payment_service.create_order({'amount': amount, 'currency':'INR','receipt':request.user.mobile,'message':f"Deposit  using rupees: {serializer.data['rupees']} -> {coin}"})
               
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
       

