"""URL routing for events application."""

from django.urls import path
from events import views

app_name = 'events'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('event/', views.EventListView.as_view(), name='event_list'),
    path('event/<int:pk>/', views.EventDetailView.as_view()),
    path('event/<int:pk>/<slug:slug>/', views.EventDetailView.as_view(), name='event'),
]
