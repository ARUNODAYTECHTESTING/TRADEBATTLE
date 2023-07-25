from django.db import models

# Create your models here.

class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Order(TimeStampModel):
    order_id = models.CharField(max_length=255)
    respose = models.JSONField()

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return self.order_id