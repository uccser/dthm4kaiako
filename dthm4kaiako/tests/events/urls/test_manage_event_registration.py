from django.urls import reverse, resolve
from http import HTTPStatus
from events.models import Event, EventRegistration
from users.models import User
from tests.dthm4kaiako_test_data_generator import (
    generate_locations,
    generate_users,
    generate_events,
    generate_addresses,
    generate_event_registrations,
    generate_serieses,
)
from tests.BaseTestWithDB import BaseTestWithDB
from users.models import User
from django.test.utils import override_settings


class ManageEventRegistrationURLTest(BaseTestWithDB):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_valid_manage_event_registration_url(self):
        generate_addresses()
        generate_serieses()
        generate_locations()
        generate_events()
        generate_users()
        generate_event_registrations()
        event = Event.objects.get(pk=1)
        registration = EventRegistration.objects.get(pk=1)
        kwargs = {
            'pk_event': event.pk,
            'pk_registration': registration.pk
            }
        url = reverse('events:manage_event_registration', kwargs=kwargs)
        expected_url = f"/events/event/{event.pk}/manage-event-registration/{registration.pk}/"
        self.assertEqual(url, expected_url)

    def test_manage_event_registration_resolve_provides_correct_view_name(self):
        generate_addresses()
        generate_serieses()
        generate_locations()
        generate_events()
        generate_users()
        generate_event_registrations()
        event = Event.objects.get(pk=1)
        registration = EventRegistration.objects.get(pk=1)
        self.assertEqual(
            resolve(f"/events/event/{event.pk}/manage-event-registration/{registration.pk}/").view_name,
            "events:manage_event_registration"
        )

    @override_settings(GOOGLE_MAPS_API_KEY="mocked")
    def test_manage_event_registration_url_returns_200_when_event_exists(self):
        generate_addresses()
        generate_serieses()
        generate_locations()
        generate_events()
        generate_users()
        generate_event_registrations()
        event = Event.objects.get(pk=1)
        user = User.objects.get(pk=1)
        event.event_staff.set([user])
        event.save()
        self.client.force_login(user)
        registration = EventRegistration.objects.get(pk=1)
        kwargs = {
            'pk_event': event.pk,
            'pk_registration': registration.pk
            }
        user = User.objects.get(pk=1)
        event.event_staff.set([user])
        event.save()
        url = reverse('events:manage_event_registration', kwargs=kwargs)
        response = self.client.post(url)
        self.assertEqual(HTTPStatus.OK, response.status_code)
