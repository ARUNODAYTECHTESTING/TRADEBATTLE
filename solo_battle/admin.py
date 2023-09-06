# admins.py

from django.contrib import admin
from .models import (
    MasterBattle, Battle, Question,
    Option, QuestionAttempt, Answer , QuestionType
)

@admin.register(MasterBattle)
class MasterBattleAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'updated_at']

@admin.register(Battle)
class BattleAdmin(admin.ModelAdmin):
    list_display = ['name', 'battle_type', 'battle_status', 'start_at', 'end_at']
    list_filter = ['battle_type', 'battle_status']

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['name', 'battle', 'question_type', 'created_at', 'updated_at']
    list_filter = ['battle', 'question_type']

@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ['name', 'question', 'created_at', 'updated_at']
    list_filter = ['question']

@admin.register(QuestionAttempt)
class QuestionAttemptAdmin(admin.ModelAdmin):
    list_display = ['user', 'question', 'option', 'created_at', 'total_number_of_entry', 'attempt']

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['user', 'option']

@admin.register(QuestionType)
class QuestionTypeAdmin(admin.ModelAdmin):
    list_display = ['name']