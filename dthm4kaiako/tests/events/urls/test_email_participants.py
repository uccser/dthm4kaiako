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

    # TODO: fix - giving 302 instead of 200
    def test_email_participants_url_returns_200_when_event_exists(self):
        generate_addresses()
        generate_serieses()
        generate_locations()
        generate_events()
        generate_users()
        generate_event_registrations()
        registration = Event.objects.get(pk=1)
        kwargs = {
            'event_pk': registration.pk,
            }
        url = reverse('events:email_participants', kwargs=kwargs)
        response = self.client.get(url)
        self.assertEqual(HTTPStatus.OK, response.status_code)
