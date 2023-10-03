from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.conf import settings
import random


# Create your models here.


class TmeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
                                      
    class Meta:
        abstract = True

class ExperienceLevel(TmeStampModel):
    name = models.CharField(max_length=50)
    point = models.IntegerField()
    color = models.CharField(max_length=64,null = True,blank = True)
    # TODO: column would be drop bcz each experience level has multiple image and it can be update after certaine level get unlock
    # image = models.ImageField(upload_to='profile_image', default='profile_image/default_image.png')

    def __str__(self) -> str:
        return self.name


class User(AbstractUser,TmeStampModel):
    GENDER = (
        (1, "MALE"), 
        (2, "FEMALE"),
        (3, "OTHERS" )
    )
    full_name = models.CharField(max_length=500, null=True, blank=True)
    dob = models.DateTimeField(null=True, blank=True)
    mobile = models.CharField(max_length=15, null=True, blank=True, unique=True, db_index=True)
    email = models.EmailField(null=True, blank=True, unique=True, db_index=True)
    gender = models.SmallIntegerField(choices=GENDER, null=True, blank=True)
    otp_code = models.CharField(max_length=10, null=True, blank=True)
    otp_created_at = models.DateTimeField(default=timezone.now)
    email_verified = models.BooleanField(default=False)
    mobile_verified = models.BooleanField(default=False)
    adhaar_number = models.CharField(max_length=16, null=True, blank=True, unique=True)
    adhaar_verified = models.BooleanField(default=False)
    pan_number = models.CharField(max_length=10, null=True, blank=True, unique=True)
    pan_verified = models.BooleanField(default=False)
    referal_code = models.CharField(max_length=20, unique=True, null=True, blank=True )
    username = models.CharField(max_length= 50, null=True, blank=True, unique=True,db_index=True)
    # TODO: added profile it can be update based on level achived and level would be multiple avtar
    active_avtar = models.CharField(null = True,blank=True,max_length = 255)
    experience_point = models.IntegerField(default=0)
    ex_level = models.ForeignKey(ExperienceLevel, on_delete=models.DO_NOTHING, null= True, blank=True)

    def send_mobile_otp(self):
        if settings.DEBUG:
            self.otp_code = "123456"
        else:
            self.otp_code = random.randint(111111, 999999)
        self.otp_created_at = timezone.now()
        self.save()
    
    def save(self, *args, **kwargs):    
        if not self.ex_level:
            default_level = ExperienceLevel.objects.filter(name__icontains="Arjuna").first()
            self.ex_level = default_level
        super().save(*args, **kwargs)




class LevelAvtar(TmeStampModel):
    image = models.ImageField(upload_to='avtar')
    name = models.CharField(max_length=64, null = True, blank = True)
    
    # TODO: Relationship
    level = models.ManyToManyField(ExperienceLevel)

    class Meta:
        ordering = ('-created_at',)