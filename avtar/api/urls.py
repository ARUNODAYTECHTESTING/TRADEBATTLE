from django.urls import path
from avtar.api import views as avtar_api_views

urlpatterns = [
    path('',avtar_api_views.AvtarView.as_view()),
    path('<int:pk>/',avtar_api_views.AvtarDetailsView.as_view()),
    path('color/',avtar_api_views.ColorPalateView.as_view()),
    path('color/<int:pk>/',avtar_api_views.ColorPalateDetailsView.as_view())
]