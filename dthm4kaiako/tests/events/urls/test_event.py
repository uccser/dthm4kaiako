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


class EventURLTest(BaseTestWithDB):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @override_settings(GOOGLE_MAPS_API_KEY="mocked")
    def test_valid_event_details_url(self):
        generate_addresses()
        generate_serieses()
        generate_locations()
        generate_events()
        generate_users()
        generate_event_registrations()
        event = Event.objects.get(pk=1)
        kwargs = {
            'pk': event.pk,
            'slug': event.slug
            }
        url = reverse('events:event', kwargs=kwargs)
        expected_url = f"/events/event/{event.pk}/{event.slug}/"
        self.assertEqual(url, expected_url)

    def test_event_details_resolve_provides_correct_view_name(self):
        generate_addresses()
        generate_serieses()
        generate_locations()
        generate_events()
        generate_users()
        event = Event.objects.get(pk=1)
        pk = event.pk
        slug = event.slug
        self.assertEqual(resolve(f"/events/event/{pk}/{slug}/").view_name, "events:event")

    @override_settings(GOOGLE_MAPS_API_KEY="mocked")
    def test_event_details_url_returns_200_when_event_exists(self):
        generate_addresses()
        generate_serieses()
        generate_locations()
        generate_events()
        generate_users()
        generate_event_registrations()
        event = Event.objects.get(pk=1)
        kwargs = {
            'pk': event.pk,
            'slug': event.slug
            }
        url = reverse('events:event', kwargs=kwargs)
        response = self.client.get(url)
        self.assertEqual(HTTPStatus.OK, response.status_code)
        