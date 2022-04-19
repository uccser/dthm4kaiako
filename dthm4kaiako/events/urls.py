"""URL routing for events application."""

from django.urls import path
from django.views.generic.base import RedirectView
from events import views

app_name = 'events'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('upcoming/', views.EventUpcomingView.as_view(), name='upcoming'),
    path('past/', views.EventPastView.as_view(), name='past'),
    path('event/<int:pk>/', views.EventDetailView.as_view()),
    path('event/<int:pk>/<slug:slug>/', views.EventDetailView.as_view(), name='event'),
    path('location/<int:pk>/', views.LocationDetailView.as_view(), name='location'),
    path('event/<int:pk>/register/', views.EventRegistrationView.as_view(), name='register'),
    path('event/<int:pk>/successful-registeration/', views.EventRegistrationSuccessView.as_view(), name='successful-registration'),
    # Redirects
    path('event/', RedirectView.as_view(pattern_name='events:home')),
    path('location/', RedirectView.as_view(pattern_name='events:home')),
]
