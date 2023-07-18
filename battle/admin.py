from django.contrib import admin
from .models import Question, Answer, Battle, RankCard
# Register your models here.

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Battle)
admin.site.register(RankCard)