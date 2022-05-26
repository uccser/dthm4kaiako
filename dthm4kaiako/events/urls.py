"""URL routing for events application."""

from django.urls import path
from django.views.generic.base import RedirectView
from events import views
from django.conf.urls import url

app_name = 'events'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('upcoming/', views.EventUpcomingView.as_view(), name='upcoming'),
    path('past/', views.EventPastView.as_view(), name='past'),
    path('event/<int:pk>/', views.EventDetailView.as_view()),
    path('event/<int:pk>/<slug:slug>/', views.EventDetailView.as_view(), name='event'),
    path('location/<int:pk>/', views.LocationDetailView.as_view(), name='location'),
    path('applications/', views.EventApplicationsView.as_view(), name='event_applications'),
    path('register/<int:pk>/', views.apply_for_event, name='apply'),

    url(r'^delete/(?P<pk>[0-9]+)/$', views.delete_event_application, name='delete_event_application'),
    

    # Redirects
    path('event/', RedirectView.as_view(pattern_name='events:home')),
    path('location/', RedirectView.as_view(pattern_name='events:home')),
]
