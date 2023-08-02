from django.shortcuts import render
from learning.serializers import QuestionSerializer
from shared.views import DropdownAPIView, PaginatedApiView
from .models import (
    Question,
    Battle,
    Stock,
    StockCategory,
    StockVariant,
    BattleType,
    ContestType,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

# Create your views here.


class QuestionVIew(PaginatedApiView):
    ModelClass = Question
    ModelSerializerClass = QuestionSerializer
    paginated_by = 100

    def get_queryset(self, request, *args, **kwargs):
        battle_id = kwargs.get("id")
        return self.ModelClass.objects.filter(battle_id=battle_id)


class ContestMeta(APIView):
    def get(self, request):
        contest_obj = ContestType.objects.all().values()
        stocks = StockVariant.objects.all().values()
        battle_obj = BattleType.objects.all().values()
        data = {
            "contest_type": list(contest_obj),
            "stock": list(stocks),
            "battle_type": list(battle_obj),
        }
        context = {"status": True, "detail": "Success", "data": data}
        return Response(context)


class VariantList(DropdownAPIView):
    serializer_fields = ["id", "name"]
    ModelClass = StockCategory


class StockList(DropdownAPIView):
    ModelClass = Stock
    serializer_fields = ["id", "image", "current_price", "movement", "move"]


    def get_queryset(self, request, *args, **kwargs):
        id = request.GET.get("id")
        variant = kwargs.get("variant")
        obj = self.ModelClass.objects.filter(variant__name = variant)
        if id:
            return obj(category_id=id)
        return obj
        

