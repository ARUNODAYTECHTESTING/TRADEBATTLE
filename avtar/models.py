from django.db import models
from authentication import models as auth_models
# Create your models here.
class TmeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
                                      
    class Meta:
        abstract = True


class LevelAvtar(TmeStampModel):
    image = models.ImageField(upload_to='avtar')
    name = models.CharField(max_length=64, null = True, blank = True)
    
    # TODO: Relationship
    level = models.ManyToManyField(auth_models.ExperienceLevel)

    class Meta:
        ordering = ('-created_at',)


    
        