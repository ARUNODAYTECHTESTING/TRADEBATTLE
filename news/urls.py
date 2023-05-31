from django.urls import path
from news import views as news_views
urlpatterns = [
    path('',news_views.NewView.as_view()),
    path('<int:id>/',news_views.NewDetailsView.as_view()),


]