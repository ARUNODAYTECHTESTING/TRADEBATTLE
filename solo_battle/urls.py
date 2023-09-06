
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BattleViewSet, MasterBattleViewSet, QuestionTypeViewSet, QuestionViewSet, OptionViewSet, QuestionAttemptViewSet , AnswerViewSet 


router = DefaultRouter()
router.register(r'master-battles', MasterBattleViewSet)
router.register(r'battles', BattleViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'options', OptionViewSet)
router.register(r'question-attempts', QuestionAttemptViewSet)
router.register(r'answers', AnswerViewSet)

urlpatterns = [
    path('', include(router.urls)),
]