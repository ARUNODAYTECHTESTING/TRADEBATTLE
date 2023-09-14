from django.contrib import admin
from django.urls import path, include

from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register(r'market_types', views.MarketTypeViewSet)
router.register(r'battle_categories', views.BattleCategoryViewSet)
router.register(r'time_battles', views.TimeBattleViewSet)
router.register(r'time_battle_users', views.TimeBattleUserViewSet)
router.register(r'solo_battles', views.SoloBattleViewSet)
router.register(r'solo_battle_users', views.SoloBattleUserViewSet)
router.register(r'league_battles', views.LeagueBattleViewSet)
router.register(r'league_battle_users', views.LeagueBattleUserViewSet)
router.register(r'question_sets', views.QuestionSetViewSet)
router.register(r'answers', views.AnswersViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
