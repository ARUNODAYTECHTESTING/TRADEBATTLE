from django.db import models
from authentication.models import User
from ckeditor.fields import RichTextField
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
    
class Pages(models.Model):
    description = RichTextField()
    page_no = models.IntegerField(default=1)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, db_index=True)

    class Meta:
        unique_together = ("page_no", "lecture")


class Question(models.Model):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, db_index=True)
    text = RichTextField()

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text =  RichTextField()
    correct = models.BooleanField(default=False)
    description = RichTextField(null=True,blank=True)




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
    quiz_atempt = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        self.video.views += 1
        self.video.save()
        super(Watchlist, self).save(*args, **kwargs)

    class Meta:
        unique_together = ("course", "video")


class BookMark(models.Model):
    
    page = models.ForeignKey(Pages, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE , db_index=True)

    class Meta:
        unique_together = ("page", "user")


    
