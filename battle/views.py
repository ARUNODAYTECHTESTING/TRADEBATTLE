from django.shortcuts import render
from learning.serializers import QuestionSerializer
from shared.views import PaginatedApiView
from .models import Question

# Create your views here.


class QuestionVIew(PaginatedApiView):

    ModelClass = Question
    ModelSerializerClass = QuestionSerializer
    paginated_by = 100

    def get_queryset(self, request, *args, **kwargs):
        battle_id = kwargs.get("id")
        return self.ModelClass.objects.filter(battle_id = battle_id)

