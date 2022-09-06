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
    path('manage/', views.EventsManagementHubView.as_view(), name='events_management_hub'),
    path('manage/<int:pk>/', views.manage_event, name='event_management'),
    url(r'^delete-via-applications/(?P<pk>[0-9]+)/$', views.delete_application_via_application_page, name='delete_application_via_application_page'),
    url(r'^delete-via-event/(?P<pk>[0-9]+)/$', views.delete_application_via_event_page, name='delete_application_via_event_page'),
    url(r'^manage-event-details/(?P<pk>[0-9]+)/$', views.manage_event_details, name='manage_event_details'),
    url(r'^manage-event-registration-form-details/(?P<pk>[0-9]+)/$', views.manage_event_registration_form_details, name='manage_event_registration_form_details'),
    url(r'^manage-event-location-details/(?P<pk>[0-9]+)/$', views.manage_event_location_details, name='manage_event_location_details'),
    url(r'^event/(?P<pk_event>[0-9]+)/manage-event-application/(?P<pk_application>[0-9]+)/$', views.manage_event_application, name='manage_event_application'),
    path('manage/mark_all_participants_as_paid/<int:pk>/', views.mark_all_participants_as_paid, name='mark_all_participants_as_paid'),
    path('manage/publish_event/<int:pk>/', views.publish_event, name='publish_event'),
    path('manage/cancel_event/<int:pk>/', views.cancel_event, name='cancel_event'),
    path('manage/generate_event_csv/', views.generate_event_csv, name='generate_event_csv'), 
    path('manage/generate_event_applications_csv/<int:pk>/', views.generate_event_applications_csv, name='generate_event_applications_csv'), 

    # Redirects
    path('event/', RedirectView.as_view(pattern_name='events:home')),
    path('location/', RedirectView.as_view(pattern_name='events:home')),
]
