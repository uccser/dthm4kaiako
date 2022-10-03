from django.test import TestCase
from django.urls import reverse, resolve
from http import HTTPStatus
from django.test.utils import override_settings
from events.models import Event
from tests.dthm4kaiako_test_data_generator import (
    generate_locations,
    generate_users,
    generate_events,
    # generate_participant_types,
    generate_addresses,
    generate_event_registrations,
    generate_serieses,
    generate_sessions
)
from users.models import User

class EventURLTest(TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @override_settings(GOOGLE_MAPS_API_KEY="mocked")
    def test_upcoming__reverse_provides_correct_url(self):
        url = reverse("events:upcoming")
        self.assertEqual(url, "/events/upcoming/")

        response = self.client.get(url)
        self.assertEqual(HTTPStatus.OK, response.status_code)

    def test_upcoming__resolve_provides_correct_view_name(self):
        self.assertEqual(resolve("/events/upcoming/").view_name, "events:upcoming")

    def test_past__reverse_provides_correct_url(self):
        self.assertEqual(reverse("events:past"), "/events/past/")

    def test_past__resolve_provides_correct_view_name(self):
        self.assertEqual(resolve("/events/past/").view_name, "events:past")

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

    @override_settings(GOOGLE_MAPS_API_KEY="mocked")
    def test_event_details_url_returns_200_when_object_exists(self):
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
        self.assertEqual(HTTPStatus.OK, response.status_code) #TODO: figure out why gives 404 - maybe not in DB?

    # TODO: fix - Failing
    def test_location(self):
        pk = 1,
        kwargs = {'pk': pk}
        url = reverse("events:location", kwargs=kwargs)
        self.assertEqual(url, "/events/location/1/")

    def test_registrations__reverse_provides_correct_url(self):
        self.assertEqual(reverse("events:event_registrations"), "/events/registrations/")

    def test_registrations__resolve_provides_correct_view_name(self):
        self.assertEqual(resolve("/events/registrations/").view_name, "events:event_registrations")

    def test_register__reverse_provides_correct_url(self):
        kwargs = {'pk': 1}
        url = reverse("events:register", kwargs=kwargs)
        self.assertEqual(url, "/events/register/1/")

    # def test_register__resolve_provides_correct_view_name(self):
    #     pass
