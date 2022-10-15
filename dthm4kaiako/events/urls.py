"""URL routing for events registration."""

from django.urls import path
from django.views.generic.base import RedirectView
from events import views
from django.conf.urls import url

app_name = 'events'
urlpatterns = [
    path(
        '',
        views.HomeView.as_view(),
        name='home'
    ),
    path(
        'upcoming/',
        views.EventUpcomingView.as_view(),
        name='upcoming'
    ),
    path(
        'past/',
        views.EventPastView.as_view(),
        name='past'
    ),
    path(
        'event/<int:pk>/',
        views.EventDetailView.as_view()
    ),
    path(
        'event/<int:pk>/<slug:slug>/',
        views.EventDetailView.as_view(),
        name='event'
    ),
    path(
        'location/<int:pk>/',
        views.LocationDetailView.as_view(),
        name='location'
    ),
    path(
        'registrations/',
        views.EventRegistrationsView.as_view(),
        name='event_registrations'
    ),
    path(
        'register/<int:pk>/',
        views.register_for_event_view,
        name='register'
    ),
    path(
        'manage/',
        views.EventsManagementView.as_view(),
        name='events_management'
    ),
    path(
        'manage/<int:pk>/',
        views.manage_event_view,
        name='event_management'
    ),
    url(
        r'^delete-via-registrations/(?P<pk>[0-9]+)/$',
        views.delete_registration_via_registration_page_view,
        name='delete_registration_via_registration_page_view'
    ),
    url(
        r'^delete-via-event/(?P<pk>[0-9]+)/$',
        views.delete_registration_via_event_page_view,
        name='delete_registration_via_event_page_view'
    ),
    url(
        r'^manage-event-details/(?P<pk>[0-9]+)/$',
        views.manage_event_details_view,
        name='manage_event_details'
    ),
    url(
        r'^manage-event-registration-form-details/(?P<pk>[0-9]+)/$',
        views.manage_event_registration_form_details_view,
        name='manage_event_registration_form_details'
    ),
    url(
        r'^event/(?P<pk_event>[0-9]+)/manage-event-registration/(?P<pk_registration>[0-9]+)/$',
        views.manage_event_registration_view,
        name='manage_event_registration'
    ),
    path(
        'manage/mark_all_participants_as_paid/<int:pk>/',
        views.mark_all_participants_as_paid_view,
        name='mark_all_participants_as_paid'
    ),
    path(
        'manage/publish_event/<int:pk>/',
        views.publish_event,
        name='publish_event'
    ),
    path(
        'manage/cancel_event/<int:pk>/',
        views.cancel_event_view,
        name='cancel_event'
    ),
    path(
        'manage/generate_event_csv/',
        views.manage_event_registration_form_details_view,
        name='generate_event_csv'
    ),
    path(
        'manage/generate_event_registrations_csv/<int:pk>/',
        views.manage_event_registration_form_details_view,
        name='generate_event_registrations_csv'
    ),
    path(
        'manage/generate_event_dietary_requirement_counts_csv/<int:pk>/',
        views.generate_event_dietary_requirement_counts_csv_view,
        name='generate_event_dietary_requirement_counts_csv'
    ),
    path(
        'manage/create_new_participant_type/<int:pk>/',
        views.create_new_participant_type_view,
        name='create_new_participant_type'
    ),
    path(
        'manage/<int:event_pk>/update_participant_type/<int:participant_type_pk>/',
        views.update_participant_type_view,
        name='update_participant_type'
    ),
    path(
        'manage/<int:event_pk>/delete_participant_type/<int:participant_type_pk>/',
        views.delete_participant_type_view,
        name='delete_participant_type'
    ),
    path(
        'manage/<int:event_pk>/email_participants/',
        views.email_participants_view,
        name='email_participants'
    ),

    # Redirects
    path(
        'event/',
        RedirectView.as_view(pattern_name='events:home')
    ),
    path(
        'location/',
        RedirectView.as_view(pattern_name='events:home')
    ),
]
