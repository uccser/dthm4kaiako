"""URL routing for events application."""

from django.urls import path
from django.views.generic.base import RedirectView, TemplateView
from events import views

app_name = 'events'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('upcoming/', views.EventUpcomingView.as_view(), name='upcoming'),
    path('past/', views.EventPastView.as_view(), name='past'),
    path('event/<int:pk>/', views.EventDetailView.as_view()),
    path('event/<int:pk>/<slug:slug>/', views.EventDetailView.as_view(), name='event'),
    path('event/', RedirectView.as_view(pattern_name='events:home'), name='event'),
    path('register/', views.EventRegistrationView.as_view(), name='register'),
    path('thanks/', TemplateView.as_view(template_name="events/thanks.html"), name='thanks'),
]
