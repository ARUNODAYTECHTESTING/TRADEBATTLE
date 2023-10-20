from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response

from battles.stock_percent import calculate_stock_percentage_with_amount
from .models import MarketType, BattleCategory, TimeBattle, TimeBattleUser, SoloBattle, SoloBattleUser, LeagueBattle, LeagueBattleUser,PredictBattleUser,PredictBattle,QuestionsBase
from .serializers import MarketTypeSerializer, BattleCategorySerializer, TimeBattleSerializer, TimeBattleUserSerializer, SoloBattleSerializer, SoloBattleUserQuestionAnswerSerializer, LeagueBattleSerializer, LeagueBattleUserSerializer, PredictBattleSerializer, PredictBattleUserSerializer,QuestionBaseSerializer
from django.views import View
from django.http import JsonResponse
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import IsAuthenticated
from .stock_data import get_stock_data
from django.utils import timezone
from django.db import transaction
from rest_framework import status
from rest_framework import generics
from battles import service as battle_service
# class MarketTypeViewSet(viewsets.ModelViewSet):
#     """API endpoint for managing MarketTypes."""

#     queryset = MarketType.objects.all()
#     serializer_class = MarketTypeSerializer


# class BattleCategoryViewSet(viewsets.ModelViewSet):
#     """API endpoint for managing BattleCategories."""

#     queryset = BattleCategory.objects.all()
#     serializer_class = BattleCategorySerializer


# class TimeBattleViewSet(viewsets.ModelViewSet):
#     """API endpoint for managing TimeBattles."""

#     queryset = TimeBattle.objects.all()
#     serializer_class = TimeBattleSerializer


# class TimeBattleUserViewSet(viewsets.ModelViewSet):
#     """API endpoint for managing TimeBattleUsers."""

#     queryset = TimeBattleUser.objects.all()
#     serializer_class = TimeBattleUserSerializer


# class SoloBattleViewSet(viewsets.ModelViewSet):
#     """API endpoint for managing SoloBattles."""

#     queryset = SoloBattle.objects.all()
#     serializer_class = SoloBattleSerializer


# class SoloBattleUserViewSet(viewsets.ModelViewSet):
#     """API endpoint for managing SoloBattleUsers."""

#     queryset = SoloBattleUser.objects.all()
#     serializer_class = SoloBattleUserSerializer




# class QuestionSetViewSet(viewsets.ModelViewSet):
#     """API endpoint for managing QuestionSets."""

#     queryset = QuestionSet.objects.all()
#     serializer_class = QuestionSetSerializer


# class AnswersViewSet(viewsets.ModelViewSet):
#     """API endpoint for managing Answers."""

#     queryset = Answers.objects.all()
#     serializer_class = AnswersSerializer


# class PredictBattleViewSet(viewsets.ModelViewSet):
#     """API endpoint for managing PredictBattles."""

#     queryset = PredictBattle.objects.all()
#     serializer_class = PredictBattleSerializer
    
# class PredictBattleUserViewSet(viewsets.ModelViewSet):
#     """API endpoint for managing PredictBattleUsers."""

#     queryset = PredictBattleUser.objects.all()
#     serializer_class = PredictBattleUserSerializer
    
    
# #League Battle
# class LeagueBattleViewSet(viewsets.ModelViewSet):
#     """API endpoint for managing LeagueBattles."""

#     queryset = LeagueBattle.objects.all()
#     serializer_class = LeagueBattleSerializer


# class LeagueBattleUserViewSet(viewsets.ModelViewSet):
#     """API endpoint for managing LeagueBattleUsers."""

#     queryset = LeagueBattleUser.objects.all()
#     serializer_class = LeagueBattleUserSerializer
    
class LeagueBattleMyBattles(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        responses={200: 'OK', 404: 'Not Found'},
        operation_summary="Get a list of league battles for My Battle section",
        operation_description="Retrieve a list of league battles with basic information.",
    )
    
    def get(self, request, *args, **kwargs):
        user = request.user
        league_battles = LeagueBattle.objects.filter(leaguebattleuser__user=user)
        battle_list = []

        for battle in league_battles:
            battle_info = {
                'battle_image': battle.battle_image.url,
                'name': battle.name,
                'max_winnings': battle.max_winnings,
                'battle_start_time': battle.battle_start_time.isoformat(),
                'battle_end_time': battle.battle_end_time.isoformat(),
                'enrollment_start_time': battle.enrollment_start_time.isoformat(),
                'enrollment_end_time': battle.enrollment_end_time.isoformat(),
                'status':battle.status
            }
            battle_list.append(battle_info)

        return JsonResponse({'league_battles': battle_list})
    
class LeagueBattleJoin(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        responses={200: 'OK', 404: 'Not Found'},
        operation_summary="Get a list of league battles for JOIN Section",
        operation_description="Retrieve a list of league battles with basic information.",
    )
    def get(self, request, *args, **kwargs):
        user = request.user
        user_joined_battles = LeagueBattleUser.objects.filter(user=user).values_list('battle_id', flat=True)
        league_battles = LeagueBattle.objects.exclude(id__in=user_joined_battles)
        battle_list = []
       

        for battle in league_battles:
            total_users = LeagueBattleUser.objects.filter(battle=battle).count()
            spots_left = battle.max_participants - total_users
            total_winners = LeagueBattleUser.objects.filter(battle=battle, coins_earned__gt=0).count()
            winner_percentage = (total_winners / total_users) * 100 if total_users > 0 else "fresh battle"
            battle_info = {
                'battle_image': battle.battle_image.url,
                'name': battle.name,
                'max_winnings': battle.max_winnings,
                'battle_start_time': battle.battle_start_time.isoformat(),
                'battle_end_time': battle.battle_end_time.isoformat(),
                'enrollment_start_time': battle.enrollment_start_time.isoformat(),
                'enrollment_end_time': battle.enrollment_end_time.isoformat(),
                'status':battle.status,
                'Number of spots left': spots_left,
                'winner_percentage': winner_percentage,
                'entry_fee':battle.entry_fee
            }
            battle_list.append(battle_info)

        return JsonResponse({'league_battles': battle_list})

class BattleDetailsView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        responses={200: 'OK', 404: 'Not Found'},
        operation_summary="Get details of a specific battle",
        operation_description="Retrieve details of a specific battle, including start and end times, enrollment details, and statistics.",
    )
    def get(self, request, *args, **kwargs):
        battle_id = self.kwargs.get('battle_id')
        try:
            battle = LeagueBattle.objects.get(pk=battle_id)
        except LeagueBattle.DoesNotExist:
            return JsonResponse({'error': 'Battle not found'}, status=404)

        total_users = LeagueBattleUser.objects.filter(battle=battle).count()
        spots_left = battle.max_participants - total_users 
        stock_data = get_stock_data()
        max_stocks = battle.max_allowed_stocks
        percentages_with_amount = calculate_stock_percentage_with_amount(max_stocks)
        print(percentages_with_amount)
 

        response_data = {
            'Category': battle.category.name,
            'Battle name': battle.name,
            'max_winnings': battle.max_winnings,
            'Start time': battle.battle_start_time.isoformat(),
            'End time': battle.battle_end_time.isoformat(),
            'Enrollment start time': battle.enrollment_start_time.isoformat(),
            'Enrollment end time': battle.enrollment_end_time.isoformat(),
            'Number of spots left': spots_left,
            'entry_fee':battle.entry_fee,
            'max_entry' : battle.max_entries,
            'stock_winning_percentage':percentages_with_amount,
            'stock_data':stock_data,
        }

        return JsonResponse(response_data)


class CreateLeagueBattleUser(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'battle_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'number_of_entries': openapi.Schema(type=openapi.TYPE_INTEGER),
                'submitted_time_and_answers': openapi.Schema(type=openapi.TYPE_OBJECT),
                'entry_fees_paid': openapi.Schema(type=openapi.TYPE_NUMBER),
            },
            required=['battle_id', 'number_of_entries', 'submitted_time_and_answers', 'entry_fees_paid'],
        ),
        responses={
            201: openapi.Response(description='Success - LeagueBattleUser created successfully'),
            400: openapi.Response(description='Bad Request - Invalid data or missing required fields'),
        },
        operation_summary="Create LeagueBattleUser",
        operation_description="Create a new LeagueBattleUser with the specified information.",
    )
    def post(self, request, *args, **kwargs):
  
        user = request.user

        data = request.data


        required_fields = ['battle_id', 'number_of_entries', 'submitted_time_and_answers', 'entry_fees_paid']
        if not all(field in data for field in required_fields):
            return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)

        battle_id = data['battle_id']
        number_of_entries = int(data['number_of_entries'])
        submitted_time_and_answers = data['submitted_time_and_answers']
        entry_fees_paid = float(data['entry_fees_paid'])

        try:
            battle = LeagueBattle.objects.get(id=battle_id)
        except LeagueBattle.DoesNotExist:
            return Response({'error': 'Invalid battle_id'}, status=status.HTTP_400_BAD_REQUEST)

        if number_of_entries > battle.max_entries:
            return Response({'error': 'Number of entries exceeds the maximum allowed'}, status=status.HTTP_400_BAD_REQUEST)


        if entry_fees_paid != (number_of_entries * battle.entry_fee):
            return Response({'error': 'Incorrect entry fee amount'}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            league_battle_user = LeagueBattleUser.objects.create(
                user=user,
                battle=battle,
                number_of_entries=number_of_entries,
                submitted_time_and_answers=submitted_time_and_answers,
                enrollment_time=timezone.now(),
                total_answer_duration=0, 
                coins_earned=0, 
                status='pending',  
                experience_points_earned=0,  
                entry_fees_paid=entry_fees_paid,
            )

        return Response({'success': 'LeagueBattleUser created successfully'}, status=status.HTTP_201_CREATED)
# TODO: Solo battle api's view

class SoloBattleQuerysetSerializerClassMixin:
    serializer_class = SoloBattleSerializer
    queryset = SoloBattle.objects.all()

class SoloBattleView(SoloBattleQuerysetSerializerClassMixin,generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]


    def post(self, request,*args,**kwargs):
        status, data = battle_service.SoloBattleService.validate_solo_battle_request(request.data)
        return Response({"status":status,"data":data},status = status)

class SoloBattleDetailsView(SoloBattleQuerysetSerializerClassMixin,generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"
    

# TODO: Question api's
class QuestionBaseQuerysetSerializerClassMixin:
    serializer_class = QuestionBaseSerializer
    queryset = QuestionsBase.objects.all()

class QuestionBaseView(QuestionBaseQuerysetSerializerClassMixin,generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    
class QuestionBaseDetailsView(QuestionBaseQuerysetSerializerClassMixin,generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"

class SoloBattleUserQuestionAnswerView(APIView):
    # TODO: Will Store enduser submitted question answer along with it's points/xp
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(request_body=SoloBattleUserQuestionAnswerSerializer)
    def post(self,request,*args,**kwargs):
        status,data = battle_service.SoloBattleUserService.validate_solo_battle_User_request(request)
        return Response({"status":status, "data":data},status=status)
