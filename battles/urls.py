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
    path('battle-details/<int:battle_id>/', LeagueBattleDetailsView.as_view(), name='battle-details'),
    path('join-league-battles/', LeagueBattleJoin.as_view(), name='all_league_battles'),
    path('my-league-battles/',LeagueBattleMyBattles.as_view(), name='my_battles'),
    path('create-league-battle-user/', CreateLeagueBattleUser.as_view(), name='create_league_battle_user'),
    # TODO: Solo battle api's urls
    # path('solo-battles/',views.SoloBattleView.as_view(), name='solo_battles'),
    # path('solo-battles/<int:pk>/',views.SoloBattleDetailsView.as_view(), name='solo_battles_detail'),
    # # TODO: QuestionBase url's
    # path('questions/',views.QuestionBaseView.as_view(), name='questions'),
    # path('questions/<int:pk>/',views.QuestionBaseDetailsView.as_view(), name='questions_details'),
    # path('solo-battle-user-question-answer/',views.SoloBattleUserQuestionAnswerView.as_view(), name='solo_battle_user_question_answer'),
    # path('solo-battle-user-question-answer/<int:pk>/',views.SoloBattleUserQuestionAnswerDetailsView.as_view(), name='solo_battle_user_question_answer_details'),
    # #Time battle urls
    path('join-time-battles/', TimeBattleJoin.as_view(), name='all_time_battles'),
    path('my-time-battles/',TimeBattleMyBattles.as_view(), name='my_time_battles'),
    path('time-battle-details/<int:battle_id>/', TimeBattleDetailsView.as_view(), name='time_battle_details'),
    path('create-time-battle-user/', CreateTimeBattleUser.as_view(), name='create_time_battle_user'),
    
    #predict battle
    path('join-predict-battles/',PredictBattleJoin.as_view(), name='predict_battles'),
    path('my-predict-battles/',PredictBattleMyBattles.as_view(), name='my_predict_battles'),
    path('predict-battle-details/<int:battle_id>/', PredictBattleDetailsView.as_view(), name='predict_battle_details'),
    path('create-predict-battle-user/', CreatePredictBattleUser.as_view(), name='create_predict_battle_user'),


]
