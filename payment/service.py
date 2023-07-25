from django.conf import settings
import razorpay

def get_client():
    client = razorpay.Client(auth=(settings.RAZORPAY_TEST_KEY_ID, settings.RAZORPAY_TEST_SECRET_ID))
    return client

def create_order(payload: dict):
    context = {
        "amount": int(payload['amount']) * 100,
        "currency": "INR",
        "receipt": payload['receipt'],
        "notes": {
            "message":payload['message'],
        }
    }
    client = get_client()
    response = client.order.create(context)
    # TODO: Response
    '''
       {'id': 'order_MI696r1CFhXQdE', 'entity': 'order', 'amount': 200, 'amount_paid': 0, 'amount_due': 200, 'currency': 'INR', 'receipt': '9137768472', 'offer_id': None, 'status': 'created', 'attempts': 0, 'notes': {'message': 'Deposit  using rupees: 2 -> 20'}, 'created_at': 1690302073}
    
    '''
    return 200, response

    