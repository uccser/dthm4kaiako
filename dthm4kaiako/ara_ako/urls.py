"""URL routing for Ara Ako application."""

from django.urls import path
from ara_ako import views

app_name = 'ara_ako'
urlpatterns = [
    path('', views.AraAkoHomeView.as_view(), name='home'),
    path('json/dashboard/', views.dashboard_json, name='dashboard_json'),
    path('<slug:slug>/', views.AraAkoEventDetailView.as_view(), name='event'),
    path('<slug:slug>/dashboard/', views.AraAkoDashboardView.as_view(), name='dashboard'),
]
