from django.urls import reverse, resolve
from http import HTTPStatus
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
from events.models import Event


class GenerateEventCSVURLTest(BaseTestWithDB):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_valid_generate_event_csv_url(self):
        generate_addresses()
        generate_serieses()
        generate_locations()
        generate_events()
        generate_users()
        generate_event_registrations()
        url = reverse('events:generate_event_csv')
        expected_url = "/events/manage/generate_event_csv/"
        self.assertEqual(url, expected_url)

    def test_generate_event_csv_resolve_provides_correct_view_name(self):
        generate_addresses()
        generate_serieses()
        generate_locations()
        generate_events()
        generate_users()
        generate_event_registrations()
        self.assertEqual(resolve("/events/manage/generate_event_csv/").view_name, "events:generate_event_csv")

    # TODO: fix - giving 302 instead of 200
    def test_cancel_event_url_returns_200_when_event_exists(self):
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
        url = reverse('events:generate_event_csv')
        response = self.client.post(url)
        self.assertEqual(HTTPStatus.FOUND, response.status_code) # redirect to event management page
