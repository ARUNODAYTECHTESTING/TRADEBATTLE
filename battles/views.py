from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from .models import MarketType, BattleCategory, TimeBattle, TimeBattleUser, SoloBattle, SoloBattleUser, LeagueBattle, LeagueBattleUser,PredictBattleUser,PredictBattle, QuestionSet, Answers
from .serializers import MarketTypeSerializer, BattleCategorySerializer, TimeBattleSerializer, TimeBattleUserSerializer, SoloBattleSerializer, SoloBattleUserSerializer, LeagueBattleSerializer, LeagueBattleUserSerializer, QuestionSetSerializer, AnswersSerializer, PredictBattleSerializer, PredictBattleUserSerializer


class MarketTypeViewSet(viewsets.ModelViewSet):
    """API endpoint for managing MarketTypes."""

    queryset = MarketType.objects.all()
    serializer_class = MarketTypeSerializer


class BattleCategoryViewSet(viewsets.ModelViewSet):
    """API endpoint for managing BattleCategories."""

    queryset = BattleCategory.objects.all()
    serializer_class = BattleCategorySerializer


class TimeBattleViewSet(viewsets.ModelViewSet):
    """API endpoint for managing TimeBattles."""

    queryset = TimeBattle.objects.all()
    serializer_class = TimeBattleSerializer


class TimeBattleUserViewSet(viewsets.ModelViewSet):
    """API endpoint for managing TimeBattleUsers."""

    queryset = TimeBattleUser.objects.all()
    serializer_class = TimeBattleUserSerializer


class SoloBattleViewSet(viewsets.ModelViewSet):
    """API endpoint for managing SoloBattles."""

    queryset = SoloBattle.objects.all()
    serializer_class = SoloBattleSerializer


class SoloBattleUserViewSet(viewsets.ModelViewSet):
    """API endpoint for managing SoloBattleUsers."""

    queryset = SoloBattleUser.objects.all()
    serializer_class = SoloBattleUserSerializer


class LeagueBattleViewSet(viewsets.ModelViewSet):
    """API endpoint for managing LeagueBattles."""

    queryset = LeagueBattle.objects.all()
    serializer_class = LeagueBattleSerializer


class LeagueBattleUserViewSet(viewsets.ModelViewSet):
    """API endpoint for managing LeagueBattleUsers."""

    queryset = LeagueBattleUser.objects.all()
    serializer_class = LeagueBattleUserSerializer


class QuestionSetViewSet(viewsets.ModelViewSet):
    """API endpoint for managing QuestionSets."""

    queryset = QuestionSet.objects.all()
    serializer_class = QuestionSetSerializer


class AnswersViewSet(viewsets.ModelViewSet):
    """API endpoint for managing Answers."""

    queryset = Answers.objects.all()
    serializer_class = AnswersSerializer


class PredictBattleViewSet(viewsets.ModelViewSet):
    """API endpoint for managing PredictBattles."""

    queryset = PredictBattle.objects.all()
    serializer_class = PredictBattleSerializer
    
class PredictBattleUserViewSet(viewsets.ModelViewSet):
    """API endpoint for managing PredictBattleUsers."""

    queryset = PredictBattleUser.objects.all()
    serializer_class = PredictBattleUserSerializer