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

class GenerateEventDietaryRequirementCountsCSVURLTest(BaseTestWithDB):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_valid_generate_event_dietary_requirement_counts_csv_url(self):
        generate_addresses()
        generate_serieses()
        generate_locations()
        generate_events()
        generate_users()
        generate_event_registrations()
        event = Event.objects.get(pk=1)
        kwargs = {
            'pk': event.pk,
            }
        url = reverse('events:generate_event_dietary_requirement_counts_csv', kwargs=kwargs)
        expected_url = f"/events/manage/generate_event_dietary_requirement_counts_csv/{event.pk}/"
        self.assertEqual(url, expected_url)

    def test_generate_event_dietary_requirement_counts_csv_resolve_provides_correct_view_name(self):
        generate_addresses()
        generate_serieses()
        generate_locations()
        generate_events()
        generate_users()
        generate_event_registrations()
        event = Event.objects.get(pk=1)
        self.assertEqual(resolve(
            f"/events/manage/generate_event_dietary_requirement_counts_csv/{event.pk}/").view_name,
            "events:generate_event_dietary_requirement_counts_csv"
            )

    def test_generate_event_dietary_requirement_counts_csv_url_returns_200_when_event_exists(self):
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
        kwargs = {
            'pk': event.pk,
            }
        url = reverse('events:generate_event_dietary_requirement_counts_csv', kwargs=kwargs)
        response = self.client.post(url)
        self.assertEqual(HTTPStatus.OK, response.status_code)
