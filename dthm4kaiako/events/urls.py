"""URL routing for events application."""

from django.urls import path
from events import views

app_name = 'events'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
]
