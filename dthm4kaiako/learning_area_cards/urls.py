"""URL routing for learning area cards application."""

from django.urls import path
from learning_area_cards import views

app_name = 'learning_area_cards'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
]
