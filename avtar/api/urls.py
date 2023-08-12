from django.urls import path
from avtar.api import views as avtar_api_views

urlpatterns = [
    path('',avtar_api_views.AvtarView.as_view()),
    path('<int:pk>/',avtar_api_views.AvtarDetailsView.as_view()),
]