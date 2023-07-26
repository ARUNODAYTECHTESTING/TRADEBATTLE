from payment import models as payment_models

def store_razorpay_order(razorpay_order):
    payment_models.Order.objects.create(order_id = razorpay_order["id"],response = razorpay_order)
