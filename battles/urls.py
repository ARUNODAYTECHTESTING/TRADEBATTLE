from django.contrib import admin
from django.urls import path, include
from .views import *

from rest_framework import routers

from . import views


router = routers.DefaultRouter()
# router.register(r'market_types', views.MarketTypeViewSet)
# router.register(r'battle_categories', views.BattleCategoryViewSet)
# router.register(r'time_battles', views.TimeBattleViewSet)
# router.register(r'time_battle_users', views.TimeBattleUserViewSet)
# router.register(r'solo_battles', views.SoloBattleViewSet)
# router.register(r'solo_battle_users', views.SoloBattleUserViewSet)
# router.register(r'league_battles', views.LeagueBattleViewSet)
# router.register(r'league_battle_users', views.LeagueBattleUserViewSet)
# router.register(r'question_sets', views.QuestionSetViewSet)
# router.register(r'answers', views.AnswersViewSet)
# router.register(r'predict_battles', views.PredictBattleViewSet)
# router.register(r'predict_battle_users', views.PredictBattleUserViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('battle-details/<int:battle_id>/', BattleDetailsView.as_view(), name='battle-details'),
    path('all_league_battles/', LeagueBattleJoin.as_view(), name='all_league_battles'),
    path('my_battles/',LeagueBattleMyBattles.as_view(), name='my_battles'),
    # TODO: Solo battle api's urls
    path('solo-battles/',views.SoloBattleView.as_view(), name='solo_battles'),
    path('solo-battles/<int:pk>/',views.SoloBattleDetailsView.as_view(), name='solo_battles_detail'),

]
