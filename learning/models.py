from django.db import models
from authentication.models import User
# Create your models here.


class Level(models.Model):

    name = models.CharField(max_length=20, unique=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='level_image', default='level_image/default_image.png')

    def __str__(self) -> str:
        return self.name


class Course(models.Model):
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    name = models.CharField(max_length=256, unique=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='banner_image', default='banner_image/default_image.png')
    fees = models.IntegerField(default=0)
    video_count = models.IntegerField(default=0)
    enrolled_user = models.IntegerField(default=0)
    extra_data = models.JSONField(null=True, blank=True)
    trailer = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self) -> str:
        return self.name
    

class Lecture(models.Model):
    title = models.CharField(max_length=1000)
    course = models.ForeignKey(Course, on_delete=models.CASCADE , db_index=True)
    video = models.CharField(max_length=1000)
    thumbnail = models.ImageField(upload_to='lecture', default='lecture/default_image.png')
    views = models.IntegerField(default=0)
    description = models.TextField(null=True, blank=True)
    extra_data = models.JSONField(null=True, blank=True)

    def __str__(self) -> str:
        return self.title

class Quiz(models.Model):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    question = models.CharField(max_length=400)
    option1 = models.CharField(max_length=400)
    option2 = models.CharField(max_length=400, default="")
    option3 = models.CharField(max_length=400,default="")
    option4 = models.CharField(max_length=400, default="")
    correctans = models.CharField(max_length=400, default="")
    description = models.TextField(null=True, blank= True)


class UserEnrolment(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index= True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.course.enrolled_user += 1
        self.course.save()
        super(UserEnrolment, self).save(*args, **kwargs)

    class Meta:
        unique_together = ("course", "user")

class Watchlist(models.Model):

    course = models.ForeignKey(UserEnrolment, on_delete=models.CASCADE ,db_index= True)
    video = models.ForeignKey(Lecture, on_delete=models.CASCADE, db_index= True)
    completed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.video.views += 1
        self.video.save()
        super(Watchlist, self).save(*args, **kwargs)

    class Meta:
        unique_together = ("course", "video")





    
