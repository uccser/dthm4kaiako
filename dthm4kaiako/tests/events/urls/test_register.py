from django.urls import reverse, resolve
from http import HTTPStatus
from events.models import Event
from tests.dthm4kaiako_test_data_generator import (
    generate_locations,
    generate_users,
    generate_events,
    generate_addresses,
    generate_serieses,
)
from tests.BaseTestWithDB import BaseTestWithDB


class RegisterURLTest(BaseTestWithDB):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_valid_register_url(self):
        generate_addresses()
        generate_serieses()
        generate_locations()
        generate_events()
        generate_users()
        event = Event.objects.get(pk=1)
        kwargs = {
            'pk': event.pk,
            }
        url = reverse('events:register', kwargs=kwargs)
        expected_url = f"/events/register/{event.pk}/"
        self.assertEqual(url, expected_url)

    def test_register_resolve_provides_correct_view_name(self):
        generate_addresses()
        generate_serieses()
        generate_locations()
        generate_events()
        generate_users()
        event = Event.objects.get(pk=1)
        pk = event.pk
        self.assertEqual(resolve(f"/events/register/{pk}/").view_name, "events:register")

    # TODO: fix - giving 302 instead of 200
    def test_register_returns_200_when_event_exists(self):
        generate_addresses()
        generate_serieses()
        generate_locations()
        generate_events()
        generate_users()
        self.client.login(id=1, password='password')
        event = Event.objects.get(pk=1)
        kwargs = {
            'pk': event.pk,
            }
        url = reverse('events:register', kwargs=kwargs)
        response = self.client.get(url)
        self.assertEqual(HTTPStatus.OK, response.status_code)
