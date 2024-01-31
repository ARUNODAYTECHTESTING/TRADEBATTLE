from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response

from battles.stock_percent import update_stock_data_percentages
from .models import MarketType, BattleCategory, TimeBattle, TimeBattleUser, SoloBattle, SoloBattleUser, LeagueBattle, LeagueBattleUser,PredictBattleUser,PredictBattle,QuestionsBase , StockData
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

class LeagueBattleDetailsView(APIView):
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
        max_stocks = battle.max_allowed_stocks

        # Fetch all StockData instances
        stock_data_list = StockData.objects.all()

        # Create a list to store the stock data
        stock_data_json = []

        # Iterate through StockData instances and append data to the list
        for stock_data in stock_data_list:
            stock_data_json.append({
                'symbol': stock_data.symbol,
                'identifier': stock_data.identifier,
                'open_price': stock_data.open_price,
                'day_high': stock_data.day_high,
                'day_low': stock_data.day_low,
                'last_price': stock_data.last_price,
                'previous_close': stock_data.previous_close,
                'change': stock_data.change,
                'p_change': stock_data.p_change,
                'year_high': stock_data.year_high,
                'year_low': stock_data.year_low,
                'total_traded_volume': stock_data.total_traded_volume,
                'total_traded_value': stock_data.total_traded_value,
                'last_update_time': stock_data.last_update_time.strftime('%Y-%m-%d %H:%M:%S'),
                'per_change_365d': stock_data.per_change_365d,
                'per_change_30d': stock_data.per_change_30d,
                'selected_percent': stock_data.selected_percent,
            })

        # Include stock data directly in the response JSON
        response_data = {
            'Category': battle.category.name,
            'Battle name': battle.name,
            'max_winnings': battle.max_winnings,
            'Start time': battle.battle_start_time.isoformat(),
            'End time': battle.battle_end_time.isoformat(),
            'Enrollment start time': battle.enrollment_start_time.isoformat(),
            'Enrollment end time': battle.enrollment_end_time.isoformat(),
            'Number of spots left': spots_left,
            'entry_fee': battle.entry_fee,
            'max_entry': battle.max_entries,
            'stock_data': stock_data_json,
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

class SoloBattleUserQuestionAnswerDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SoloBattleUser.objects.all()
    serializer_class = SoloBattleUserQuestionAnswerSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"
    


#time battle

class TimeBattleMyBattles(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        responses={200: 'OK', 404: 'Not Found'},
        operation_summary="Get a list of time battles for My Battle section",
        operation_description="Retrieve a list of time battles with basic information.",
    )
    
    def get(self, request, *args, **kwargs):
        user = request.user
        league_battles = TimeBattle.objects.filter(timebattleuser__user=user)
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

        return JsonResponse({'time_battles': battle_list})
    
class TimeBattleJoin(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        responses={200: 'OK', 404: 'Not Found'},
        operation_summary="Get a list of time battles for JOIN Section",
        operation_description="Retrieve a list of time battles with basic information.",
    )
    def get(self, request, *args, **kwargs):
        user = request.user
        user_joined_battles = TimeBattleUser.objects.filter(user=user).values_list('battle_id', flat=True)
        time_battles = TimeBattle.objects.exclude(id__in=user_joined_battles)
        battle_list = []
       

        for battle in time_battles:
            total_users = TimeBattleUser.objects.filter(battle=battle).count()
            spots_left = battle.max_participants - total_users
            total_winners = TimeBattleUser.objects.filter(battle=battle, coins_earned__gt=0).count()
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

        return JsonResponse({'time_battles': battle_list})
    

class TimeBattleDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: 'OK', 404: 'Not Found'},
        operation_summary="Get details of a specific battle",
        operation_description="Retrieve details of a specific battle, including start and end times, enrollment details, and statistics.",
    )
    def get(self, request, *args, **kwargs):
        battle_id = self.kwargs.get('battle_id')
        try:
            battle = TimeBattle.objects.get(pk=battle_id)
        except TimeBattle.DoesNotExist:
            return Response({'error': 'Battle not found'}, status=status.HTTP_404_NOT_FOUND)

        total_users = TimeBattleUser.objects.filter(battle=battle).count()
        spots_left = battle.max_participants - total_users 

        # Retrieve all questions associated with the battle
        questions = QuestionsBase.objects.filter(id__in=battle.questions_set.all())

        # Construct the response JSON
        response_data = {
            'Category': battle.category.name,
            'Battle name': battle.name,
            'max_winnings': battle.max_winnings,
            'Start time': battle.battle_start_time.isoformat(),
            'End time': battle.battle_end_time.isoformat(),
            'Enrollment start time': battle.enrollment_start_time.isoformat(),
            'Enrollment end time': battle.enrollment_end_time.isoformat(),
            'Number of spots left': spots_left,
            'entry_fee': battle.entry_fee,
            'Questions': [
                {
                    'name': question.name,
                    'options': question.options,
                    'correct_answer': question.correct_answer,
                }
                for question in questions
            ],
        }

        return Response(response_data, status=status.HTTP_200_OK)



class CreateTimeBattleUser(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'battle_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'number_of_entries': openapi.Schema(type=openapi.TYPE_INTEGER),
                'submitted_time_and_answers': openapi.Schema(type=openapi.TYPE_OBJECT),
                'entry_fees_paid': openapi.Schema(type=openapi.TYPE_STRING), 
            },
            required=['battle_id', 'number_of_entries', 'submitted_time_and_answers', 'entry_fees_paid'],
        ),
        responses={
            201: openapi.Response(description='Success - TimeBattleUser created successfully'),
            400: openapi.Response(description='Bad Request - Invalid data or missing required fields'),
        },
        operation_summary="Create TimeBattleUser",
        operation_description="Create a new TimeBattleUser with the specified information.",
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
            battle = TimeBattle.objects.get(id=battle_id)
        except TimeBattle.DoesNotExist:
            return Response({'error': 'Invalid battle_id'}, status=status.HTTP_400_BAD_REQUEST)

        if entry_fees_paid != (number_of_entries * battle.entry_fee):
            return Response({'error': 'Incorrect entry fee amount'}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            time_battle_user = TimeBattleUser.objects.create(
                user=user,
                battle=battle,
                submitted_time_and_answers=data['submitted_time_and_answers'],
                enrollment_time=timezone.now(),
                total_answer_duration=0, 
                coins_earned=0, 
                status='pending',  
                experience_points_earned=0,  
                entry_fees_paid=data['entry_fees_paid'],
            )

        return Response({'success': 'TimeBattleUser created successfully'}, status=status.HTTP_201_CREATED)
    
    
    
# TODO: predict battle api's view

class PredictBattleMyBattles(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: 'OK', 404: 'Not Found'},
        operation_summary="Get a list of predict battles for My Battle section",
        operation_description="Retrieve a list of predict battles with basic information.",
    )
    def get(self, request, *args, **kwargs):
        user = request.user
        predict_battles = PredictBattle.objects.filter(predictbattleuser__user=user)
        battle_list = []

        for battle in predict_battles:
            battle_info = {
                'battle_image': battle.battle_image.url,
                'name': battle.name,
                'max_winnings': battle.max_winnings,
                'battle_start_time': battle.battle_start_time.isoformat(),
                'battle_end_time': battle.battle_end_time.isoformat(),
                'enrollment_start_time': battle.enrollment_start_time.isoformat(),
                'enrollment_end_time': battle.enrollment_end_time.isoformat(),
                'status': battle.status
            }
            battle_list.append(battle_info)

        return JsonResponse({'predict_battles': battle_list})


class PredictBattleJoin(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: 'OK', 404: 'Not Found'},
        operation_summary="Get a list of predict battles for JOIN Section",
        operation_description="Retrieve a list of predict battles with basic information.",
    )
    def get(self, request, *args, **kwargs):
        user = request.user
        user_joined_battles = PredictBattleUser.objects.filter(user=user).values_list('battle_id', flat=True)
        predict_battles = PredictBattle.objects.exclude(id__in=user_joined_battles)
        battle_list = []

        for battle in predict_battles:
            total_users = PredictBattleUser.objects.filter(battle=battle).count()
            spots_left = battle.max_participants - total_users
            battle_info = {
                'battle_image': battle.battle_image.url,
                'name': battle.name,
                'max_winnings': battle.max_winnings,
                'battle_start_time': battle.battle_start_time.isoformat(),
                'battle_end_time': battle.battle_end_time.isoformat(),
                'enrollment_start_time': battle.enrollment_start_time.isoformat(),
                'enrollment_end_time': battle.enrollment_end_time.isoformat(),
                'status': battle.status,
                'Number of spots left': spots_left,
                'entry_fee': battle.entry_fee
            }
            battle_list.append(battle_info)

        return JsonResponse({'predict_battles': battle_list})


class PredictBattleDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: 'OK', 404: 'Not Found'},
        operation_summary="Get details of a specific battle",
        operation_description="Retrieve details of a specific predict battle, including start and end times, enrollment details, and statistics.",
    )
    def get(self, request, *args, **kwargs):
        battle_id = self.kwargs.get('battle_id')
        try:
            battle = PredictBattle.objects.get(pk=battle_id)
        except PredictBattle.DoesNotExist:
            return JsonResponse({'error': 'Battle not found'}, status=404)

        total_users = PredictBattleUser.objects.filter(battle=battle).count()
        spots_left = battle.max_participants - total_users

        # Include additional details specific to PredictBattle if needed

        response_data = {
            'Category': battle.category.name,
            'Battle name': battle.name,
            'max_winnings': battle.max_winnings,
            'Start time': battle.battle_start_time.isoformat(),
            'End time': battle.battle_end_time.isoformat(),
            'Enrollment start time': battle.enrollment_start_time.isoformat(),
            'Enrollment end time': battle.enrollment_end_time.isoformat(),
            'Number of spots left': spots_left,
            'entry_fee': battle.entry_fee,
        }

        return JsonResponse(response_data)


class CreatePredictBattleUser(APIView):
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
            201: openapi.Response(description='Success - PredictBattleUser created successfully'),
            400: openapi.Response(description='Bad Request - Invalid data or missing required fields'),
        },
        operation_summary="Create PredictBattleUser",
        operation_description="Create a new PredictBattleUser with the specified information.",
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
            battle = PredictBattle.objects.get(id=battle_id)
        except PredictBattle.DoesNotExist:
            return Response({'error': 'Invalid battle_id'}, status=status.HTTP_400_BAD_REQUEST)

        if entry_fees_paid != (number_of_entries * battle.entry_fee):
            return Response({'error': 'Incorrect entry fee amount'}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            predict_battle_user = PredictBattleUser.objects.create(
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

        return Response({'success': 'PredictBattleUser created successfully'}, status=status.HTTP_201_CREATED)
