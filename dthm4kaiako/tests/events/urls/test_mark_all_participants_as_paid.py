from django.urls import reverse, resolve
from http import HTTPStatus
from events.models import Event
from users.models import User
from tests.dthm4kaiako_test_data_generator import (
    generate_locations,
    generate_users,
    generate_events,
    generate_addresses,
    generate_serieses,
)
from tests.BaseTestWithDB import BaseTestWithDB


class MarkAllParticipantsAsPaidURLTest(BaseTestWithDB):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_valid_mark_all_participants_as_paid_url(self):
        generate_addresses()
        generate_serieses()
        generate_locations()
        generate_events()
        generate_users()
        event = Event.objects.get(pk=1)
        kwargs = {
            'pk': event.pk,
            }
        url = reverse('events:mark_all_participants_as_paid', kwargs=kwargs)
        expected_url = f"/events/manage/mark_all_participants_as_paid/{event.pk}/"
        self.assertEqual(url, expected_url)

    def test_mark_all_participants_as_paid_resolve_provides_correct_view_name(self):
        generate_addresses()
        generate_serieses()
        generate_locations()
        generate_events()
        generate_users()
        event = Event.objects.get(pk=1)
        self.assertEqual(
            resolve(f"/events/manage/mark_all_participants_as_paid/{event.pk}/").view_name,
            "events:mark_all_participants_as_paid"
        )

    # TODO: fix - giving 302 instead of 200
    def test_mark_all_participants_as_paid_url_returns_200_when_event_exists(self):
        generate_addresses()
        generate_serieses()
        generate_locations()
        generate_events()
        generate_users()
        event = Event.objects.get(pk=1)
        kwargs = {
            'pk': event.pk,
            }
        user = User.objects.get(pk=1)
        event.event_staff.set([user])
        event.save()
        url = reverse('events:mark_all_participants_as_paid', kwargs=kwargs)
        response = self.client.get(url)
        self.assertEqual(HTTPStatus.OK, response.status_code)
