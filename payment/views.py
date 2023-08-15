from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.conf import settings
from payment import service as payment_service
from rest_framework.response import Response
import json
from payment import query

# Create your views here.
def load_payment_page(request):
    return render(request, 'payment.html', {})


class PaymentCallBackview(APIView):
    permission_classes = (AllowAny,)

    def post(self, request,*args, **kwargs):
        try:
            webhook_body = request.body.decode("utf-8")
            webhook_signature = request.headers["X-Razorpay-Signature"]
            webhook_secret = settings.RAZORPAY_WEBHOOK_KEY_SECRET
            client = payment_service.get_client()
            if not client.utility.verify_webhook_signature(webhook_body, webhook_signature, webhook_secret):
                return Response({"status":400,"message":"not authorized webhook"})
            json_data = json.loads(webhook_body)
            if json_data["event"] in ["payment.captured"]:
                query.create_payment(json_data)

        except Exception as e:
            return Response({"status": 400, "detail": f"{e}"},status=400)

        finally:
            return Response({"status":"success","detail":"Payment successfull"},status=200)
                    
