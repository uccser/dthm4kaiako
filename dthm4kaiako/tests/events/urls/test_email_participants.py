from django.urls import reverse, resolve
from http import HTTPStatus
from events.models import Event
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


class EmailParticipantsURLTest(BaseTestWithDB):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_valid_email_participants_url(self):
        generate_addresses()
        generate_serieses()
        generate_locations()
        generate_events()
        generate_users()
        generate_event_registrations()
        event = Event.objects.get(pk=1)
        kwargs = {
            'event_pk': event.pk,
            }
        url = reverse('events:email_participants', kwargs=kwargs)
        expected_url = f"/events/manage/{event.pk}/email_participants/"
        self.assertEqual(url, expected_url)

    def test_email_participants_resolve_provides_correct_view_name(self):
        generate_addresses()
        generate_serieses()
        generate_locations()
        generate_events()
        generate_users()
        generate_event_registrations()
        registration = Event.objects.get(pk=1)
        self.assertEqual(
            resolve(f"/events/manage/{registration.pk}/email_participants/").view_name,
            "events:email_participants"
        )

    @override_settings(GOOGLE_MAPS_API_KEY="mocked")
    def test_email_participants_url_returns_200_when_event_exists(self):
        generate_addresses()
        generate_serieses()
        generate_locations()
        generate_events()
        generate_users()
        generate_event_registrations()
        user = User.objects.get(id=1)
        self.client.force_login(user)
        event = Event.objects.get(pk=1)
        event.event_staff.set([user])
        event.save()
        kwargs = {
            'event_pk': event.pk,
            }
        url = reverse('events:email_participants', kwargs=kwargs)
        response = self.client.post(url)
        self.assertEqual(HTTPStatus.OK, response.status_code)
