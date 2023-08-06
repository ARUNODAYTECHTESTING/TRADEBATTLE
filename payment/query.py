from payment import models as payment_models

def store_razorpay_order(razorpay_order):
    payment_models.Order.objects.create(order_id = razorpay_order["id"],response = razorpay_order)


def update_razorpay_order_status(order_id,status):
    print("update razorpay order execute !!")
    payment_models.Order.objects.filter(order_id=order_id).update(status=status)


def create_payment(payload):
    print("create payment execute!!")
    payment_models.Payment.objects.create(
        order_id=payload["order_id"],
        payment_id=payload["id"],
        response=payload
    )
    update_razorpay_order_status(payload["order_id"],"COMPLETED")    
     
    
