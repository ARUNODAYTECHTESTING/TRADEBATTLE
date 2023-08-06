from django.db import models
from authentication import models as auth_models

# Create your models here.

class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Order(TimeStampModel):
    ORDER_STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed'),
    )
    user = models.ForeignKey(auth_models.User, related_name="orders",on_delete=models.CASCADE,null=True,blank=True),
    order_id = models.CharField(max_length=255)
    response = models.JSONField()
    status = models.CharField(choices=ORDER_STATUS_CHOICES,default="PENDING",max_length=64)

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return self.order_id
    

class Payment(TimeStampModel):
    order_id = models.ForeignKey(Order, related_name='payment',on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=255)
    response = models.JSONField()



    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return self.payment_id