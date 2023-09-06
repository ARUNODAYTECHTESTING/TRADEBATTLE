from django.shortcuts import render
from rest_framework import viewsets
from .models import Answer, Battle, MasterBattle, QuestionType, Question, Option, QuestionAttempt
from .serializers import AnswerSerializer, BattleSerializer, MasterBattleSerializer, QuestionTypeSerializer, QuestionSerializer, OptionSerializer, QuestionAttemptSerializer



class MasterBattleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MasterBattle.objects.all()
    serializer_class = MasterBattleSerializer
    
    
class BattleViewSet(viewsets.ModelViewSet):
    queryset = Battle.objects.all()
    serializer_class = BattleSerializer


class QuestionTypeViewSet(viewsets.ModelViewSet):
    queryset = QuestionType.objects.all()
    serializer_class = QuestionTypeSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class OptionViewSet(viewsets.ModelViewSet):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer


class QuestionAttemptViewSet(viewsets.ModelViewSet):
    queryset = QuestionAttempt.objects.all()
    serializer_class = QuestionAttemptSerializer

class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
