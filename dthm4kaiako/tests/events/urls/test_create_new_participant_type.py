from django.urls import reverse, resolve
from http import HTTPStatus
from events.models import Event
from tests.dthm4kaiako_test_data_generator import (
    generate_locations,
    generate_users,
    generate_events,
    generate_addresses,
    generate_serieses,
    generate_participant_types,
)
from tests.BaseTestWithDB import BaseTestWithDB


class CreateNewParticipantTypeURLTest(BaseTestWithDB):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_valid_create_new_participant_type_url(self):
        generate_addresses()
        generate_serieses()
        generate_locations()
        generate_events()
        generate_users()
        generate_participant_types()
        event = Event.objects.get(pk=1)
        kwargs = {
            'pk': event.pk,
            }
        url = reverse('events:create_new_participant_type', kwargs=kwargs)
        expected_url = f"/events/manage/create_new_participant_type/{event.pk}/"
        self.assertEqual(url, expected_url)

    def test_create_new_participant_type_resolve_provides_correct_view_name(self):
        generate_addresses()
        generate_serieses()
        generate_locations()
        generate_events()
        generate_users()
        generate_participant_types()
        event = Event.objects.get(pk=1)
        self.assertEqual(resolve(
            f"/events/manage/create_new_participant_type/{event.pk}/").view_name,
            "events:create_new_participant_type"
        )

    # TODO: fix - giving 302 instead of 200
    def test_create_new_participant_type_url_returns_200_when_event_exists(self):
        generate_addresses()
        generate_serieses()
        generate_locations()
        generate_events()
        generate_users()
        generate_participant_types()
        event = Event.objects.get(pk=1)
        kwargs = {
            'pk': event.pk,
            }
        url = reverse('events:create_new_participant_type', kwargs=kwargs)
        response = self.client.get(url)
        self.assertEqual(HTTPStatus.OK, response.status_code)
