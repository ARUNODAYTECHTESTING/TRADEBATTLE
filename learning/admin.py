from django.contrib import admin
from .models import (
    Level,
    Course,
    Lecture,
    Watchlist,
    Quiz
)
# Register your models here.

admin.site.register(Course)
admin.site.register(Level)
admin.site.register(Lecture)
admin.site.register(Watchlist)
admin.site.register(Quiz)
