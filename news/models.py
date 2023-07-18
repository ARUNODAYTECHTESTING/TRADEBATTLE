from django.db import models
from core import storage_backends
from django.contrib.postgres.fields import ArrayField


# Create your models here.
class TimeStamModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(TimeStamModel):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self) -> str:
        return self.name
    

class News(TimeStamModel):
    news = ArrayField(models.CharField(max_length=255),null=True,blank=True)
    category = models.ForeignKey(Category,related_name="news",null=True,blank=True,on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at']


class Stock(TimeStamModel):
    stock = models.CharField(max_length=64)
    category = models.ForeignKey(Category,related_name="stocks",null=True,blank=True,on_delete=models.CASCADE)



