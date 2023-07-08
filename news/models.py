from django.db import models
from core import storage_backends
# Create your models here.
class TimeStamModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class News(TimeStamModel):
    head_line = models.CharField(max_length=248)
    description = models.TextField()
    published_date = models.DateField()
    pulisher  = models.CharField(max_length=64)
    image = models.ImageField(upload_to=storage_backends.PublicMediaStorage(),null=True,blank=True)

    class Meta:
        ordering = ['-created_at']