from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK
)
from rest_framework.views import APIView
from .models import Referal
from authentication.models import User
from wallet import service as wallet_service

# Create your views here.



class ReferalView(APIView):
    def post(self, request):
        res_status = HTTP_400_BAD_REQUEST
        output_status = False
        message = "failed"
        referal_code = request.data.get("referal_code")
        if referal_code:
            other_user = User.objects.filter(username=referal_code)
            if other_user.exists():
                other_user = other_user.first()
                try:
                    Referal.objects.create(referer_id=other_user.id,user_id=request.user.id)

                    # Uncomment when wallet is implemented
                    # try:
                    #     wallet = Wallet.objects.get(user_id=other_user.id)
                    # except Wallet.DoesNotExist:
                    #     wallet = Wallet.objects.create(user_id=other_user.id)
                    # obj = Transaction.objects.create(
                    #     wallet=wallet,
                    #     amount=config("REFERRAL_AMOUNT", default=250),
                    #     message=f"Referral Bonus for {request.user.full_name}",
                    #     action=1,  # credit
                    #     credit_type=3,  # referral
                    # ) 
                    res_status = HTTP_200_OK
                    output_status = True
                    message = "Referal Successful"
                except Exception as e:
                    message = "Something Unexpected happened"
            else:
                message = "Invalid referal code"
        else:
            message = "referal code is required"
        context = {"status": output_status, "message": message}
        return Response(context, status=res_status, content_type="application/json")

class TransactionView(APIView):
    

    def post(self, request,credit_type, *args, **kwargs):
        try:
            status, data = wallet_service.WalletService.validate_transaction_request(request.data,int(credit_type))

        except Exception as e:
            status , data = 400, f"{e}"

        finally:
            return Response({"status":status,"details":data},status = status)