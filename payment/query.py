from payment import models as payment_models

def store_razorpay_order(razorpay_order):
    payment_models.Order.objects.create(order_id = razorpay_order["id"],response = razorpay_order)


def update_razorpay_order(payload):
    print("update razorpay order execute !!")
    pass


def create_payment(payload):
    print("create payment execute")
    pass

