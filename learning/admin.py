from django.contrib import admin
from .models import (
    Level,
    Course,
    Lecture,
    Watchlist,
    Question,
    Answer,
    UserEnrolment,
    BookMark,
    Pages,
)

# Register your models here.

admin.site.register(Course)
admin.site.register(Level)
admin.site.register(Lecture)
admin.site.register(Watchlist)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(UserEnrolment)
admin.site.register(Pages)
