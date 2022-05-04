"""URL routing for get_started application."""

from django.urls import path
from get_started import views

app_name = 'get_started'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('<slug:slug>/', views.ComponentDetailView.as_view(), name='component'),
]
