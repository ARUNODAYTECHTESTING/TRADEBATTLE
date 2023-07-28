from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
# Create your views here.
def load_payment_page(request):
    return render(request, 'payment.html', {})


class PaymentCallBackview(APIView):
    permission_classes = (AllowAny,)

    def post(self, request,*args, **kwargs):
        try:
            print("Payment CallBack executed successfully")

        except Exception as e:
            pass

        finally:
            pass