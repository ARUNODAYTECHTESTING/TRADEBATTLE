from django.shortcuts import render

# Create your views here.
def load_payment_page(request):
    return render(request, 'payment.html', {})