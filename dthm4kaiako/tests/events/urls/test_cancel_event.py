from django.urls import reverse, resolve
from http import HTTPStatus
from events.models import Event
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


class CancelEventURLTest(BaseTestWithDB):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_valid_cancel_event_url(self):
        generate_addresses()
        generate_serieses()
        generate_locations()
        generate_events()
        generate_users()
        event = Event.objects.get(pk=1)
        kwargs = {
            'pk': event.pk,
            }
        updated_event = Event.objects.filter(pk=1)
        updated_event.update(published=True)
        event.save()
        url = reverse('events:cancel_event', kwargs=kwargs)
        expected_url = f"/events/manage/cancel_event/{event.pk}/"
        self.assertEqual(url, expected_url)

    def test_cancel_event_resolve_provides_correct_view_name(self):
        generate_addresses()
        generate_serieses()
        generate_locations()
        generate_events()
        generate_users()
        generate_event_registrations()
        event = Event.objects.get(pk=1)
        updated_event = Event.objects.filter(pk=1)
        updated_event.update(published=True)
        event.save()
        self.assertEqual(resolve(f"/events/manage/cancel_event/{event.pk}/").view_name, "events:cancel_event")

    # TODO: fix - giving 302 instead of 200
    def test_cancel_event_url_returns_200_when_event_exists(self):
        generate_addresses()
        generate_serieses()
        generate_locations()
        generate_events()
        generate_users()
        generate_event_registrations()
        event = Event.objects.get(pk=1)
        updated_event = Event.objects.filter(pk=1)
        updated_event.update(published=True)
        kwargs = {
            'pk': event.pk,
            }
        user = User.objects.get(pk=1)
        event.event_staff.set([user])
        event.save()
        url = reverse('events:cancel_event', kwargs=kwargs)
        response = self.client.get(url)
        self.assertEqual(HTTPStatus.OK, response.status_code)
