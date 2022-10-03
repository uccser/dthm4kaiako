from django.urls import reverse, resolve
from http import HTTPStatus
from django.test.utils import override_settings
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


class EventsManagementURLTest(BaseTestWithDB):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_valid_events_management_url(self):
        url = reverse('events:events_management')
        expected_url = f"/events/manage/"
        self.assertEqual(url, expected_url)

    def test_events_management_resolve_provides_correct_view_name(self):
        self.assertEqual(resolve(f"/events/manage/").view_name, "events:events_management")

    # TODO: fix - giving 302 instead of 200
    def test_events_management_returns_200_when_event_exists(self):
        url = reverse('events:events_management')
        response = self.client.get(url)
        self.assertEqual(HTTPStatus.OK, response.status_code)
