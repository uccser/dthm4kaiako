"""URL routing for Ara Ako application."""

from django.urls import path
from ara_ako import views

app_name = 'ara_ako'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
]
