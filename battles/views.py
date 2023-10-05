from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from .models import MarketType, BattleCategory, TimeBattle, TimeBattleUser, SoloBattle, SoloBattleUser, LeagueBattle, LeagueBattleUser,PredictBattleUser,PredictBattle, QuestionSet, Answers
from .serializers import MarketTypeSerializer, BattleCategorySerializer, TimeBattleSerializer, TimeBattleUserSerializer, SoloBattleSerializer, SoloBattleUserSerializer, LeagueBattleSerializer, LeagueBattleUserSerializer, QuestionSetSerializer, AnswersSerializer, PredictBattleSerializer, PredictBattleUserSerializer
from django.views import View
from django.http import JsonResponse

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
    
    
#League Battle
class LeagueBattleViewSet(viewsets.ModelViewSet):
    """API endpoint for managing LeagueBattles."""

    queryset = LeagueBattle.objects.all()
    serializer_class = LeagueBattleSerializer


class LeagueBattleUserViewSet(viewsets.ModelViewSet):
    """API endpoint for managing LeagueBattleUsers."""

    queryset = LeagueBattleUser.objects.all()
    serializer_class = LeagueBattleUserSerializer
    
class LeagueBattleListAll(View):
    def get(self, request, *args, **kwargs):
        league_battles = LeagueBattle.objects.all()
        battle_list = []

        for battle in league_battles:
            battle_info = {
                'battle_image': battle.battle_image.url,
                'name': battle.name,
                'battle_start_time': battle.battle_start_time.isoformat(),
                'battle_end_time': battle.battle_end_time.isoformat(),
                'enrollment_start_time': battle.enrollment_start_time.isoformat(),
                'enrollment_end_time': battle.enrollment_end_time.isoformat(),
            }
            battle_list.append(battle_info)

        return JsonResponse({'league_battles': battle_list})
    

class BattleDetailsView(View):
    def get(self, request, *args, **kwargs):
        # Assuming you have battle_id in the URL parameters
        battle_id = self.kwargs.get('battle_id')
        
        try:
            battle = LeagueBattle.objects.get(pk=battle_id)
        except LeagueBattle.DoesNotExist:
            return JsonResponse({'error': 'Battle not found'}, status=404)

        # Calculate number of spots left
        total_users = LeagueBattleUser.objects.filter(battle=battle).count()
        spots_left = battle.max_participants - total_users

        # Calculate winner percentage
        total_winners = LeagueBattleUser.objects.filter(battle=battle, coins_earned__gt=0).count()
        winner_percentage = (total_winners / total_users) * 100 if total_users > 0 else 0

        # Build the response
        response_data = {
            'Category': battle.category.name,
            'Battle name': battle.name,
            'Start time': battle.battle_start_time.isoformat(),
            'End time': battle.battle_end_time.isoformat(),
            'Enrollment start time': battle.enrollment_start_time.isoformat(),
            'Enrollment end time': battle.enrollment_end_time.isoformat(),
            'Number of spots left': spots_left,
            'Winner %': winner_percentage,
        }

        return JsonResponse(response_data)
