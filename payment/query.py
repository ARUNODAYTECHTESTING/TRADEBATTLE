from payment import models as payment_models
from wallet import query as wallet_query

def store_razorpay_order(razorpay_order,user):
    payment_models.Order.objects.create(order_id = razorpay_order["id"],response = razorpay_order,user = user)

def get_order_by_id(order_id):
    return payment_models.Order.objects.filter(order_id = order_id).first()

def update_razorpay_order_status(order_id,status):
    print("update razorpay order execute !!")
    payment_models.Order.objects.filter(order_id=order_id).update(status=status)


def create_payment(data):
    print("create payment execute!!!!!!!!")    
    # {'entity': 'event', 'account_id': 'acc_Ja7clXrWRXJTJC', 'event': 'payment.captured', 'contains': ['payment'], 'payload': {'payment': {'entity': {'id': 'pay_MNZ8MAx2U2aTed', 'entity': 'payment', 'amount': 100, 'currency': 'INR', 'status': 'captured', 'order_id': 'order_MNZ7pBu00vqFc9', 'invoice_id': None, 'international': False, 'method': 'wallet', 'amount_refunded': 0, 'refund_status': None, 'captured': True, 'description': 'Test Transaction', 'card_id': None, 'bank': None, 'wallet': 'mobikwik', 'vpa': None, 'email': 'gaurav.kumar@example.com', 'contact': '+919000090000', 'notes': {'message': 'Deposit  using rupees: 1 -> 10', 'address': 'Razorpay Corporate Office'}, 'fee': 2, 'tax': 0, 'error_code': None, 'error_description': None, 'error_source': None, 'error_step': None, 'error_reason': None, 'acquirer_data': {'transaction_id': None}, 'created_at': 1691495857, 'base_amount': 100}}}, 'created_at': 1691495861}
    order = get_order_by_id(data['payload']['payment']['entity']["order_id"])
    # TODO: create payment 
    payment_models.Payment.objects.create(order=order,payment_id=data['payload']['payment']['entity']["id"],response=data)
    # TODO: order update to completed
    update_razorpay_order_status(order.order_id,"COMPLETED")
    # TODO: create wallet for current user
    wallet,created = wallet_query.create_user_wallet(order.user)
    # TODO: create transaction
    amount = int(order.response["amount"])/100
    wallet_query.create_transaction(wallet = wallet,credit_type = 1,action = 1, amount=amount)
     
     
    
