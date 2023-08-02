from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.conf import settings
import random


# Create your models here.



class ExperienceLevel(models.Model):
    name = models.CharField(max_length=50)
    point = models.IntegerField()
    # TODO: column would be drop bcz each experience level has multiple image and it can be update after certaine level get unlock
    # image = models.ImageField(upload_to='profile_image', default='profile_image/default_image.png')

    def __str__(self) -> str:
        return self.name


class User(AbstractUser):
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
    image = models.ImageField(upload_to='profile_image', default='profile_image/default_image.png')
    experience_point = models.IntegerField(default=0)
    ex_level = models.ForeignKey(ExperienceLevel, on_delete=models.DO_NOTHING, null= True, blank=True)

    def send_mobile_otp(self):
        if settings.DEBUG:
            self.otp_code = "123456"
        else:
            self.otp_code = random.randint(111111, 999999)
        self.otp_created_at = timezone.now()
        self.save()