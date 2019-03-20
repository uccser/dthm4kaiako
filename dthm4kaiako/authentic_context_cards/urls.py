"""URL routing for DTTA application."""

from django.urls import path
from authentic_context_cards import views

app_name = 'authentic_context_cards'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('download/', views.generate_cards, name="download"),
]
