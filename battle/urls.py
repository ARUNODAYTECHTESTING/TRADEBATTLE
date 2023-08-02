from django.urls import path
from .views import (
    ContestMeta,
    VariantList,
    StockList,
    QuestionVIew
)


urlpatterns = [
    path("contest-meta/", ContestMeta.as_view()),
    path("variant-list/", VariantList.as_view()),
    path("stock-list/<variant>/", StockList.as_view()),
    path("question-list/<id>/", QuestionVIew.as_view())
]