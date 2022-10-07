from django.urls import reverse, resolve
from http import HTTPStatus
from events.models import Event, ParticipantType
from tests.dthm4kaiako_test_data_generator import (
    generate_locations,
    generate_users,
    generate_events,
    generate_addresses,
    generate_serieses,
    generate_participant_types,
)
from tests.BaseTestWithDB import BaseTestWithDB
from users.models import User


class DeleteParticipantTypeURLTest(BaseTestWithDB):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_valid_delete_participant_type_url(self):
        generate_addresses()
        generate_serieses()
        generate_locations()
        generate_events()
        generate_users()
        generate_participant_types()
        event = Event.objects.get(pk=1)
        participant_type = ParticipantType.objects.get(pk=1)
        kwargs = {
            'event_pk': event.pk,
            'participant_type_pk': participant_type.pk
            }
        url = reverse('events:delete_participant_type', kwargs=kwargs)
        expected_url = f"/events/manage/{event.pk}/delete_participant_type/{participant_type.pk}/"
        self.assertEqual(url, expected_url)

    def test_delete_participant_type_resolve_provides_correct_view_name(self):
        generate_addresses()
        generate_serieses()
        generate_locations()
        generate_events()
        generate_users()
        generate_participant_types()
        event = Event.objects.get(pk=1)
        participant_type = ParticipantType.objects.get(pk=1)
        self.assertEqual(
            resolve(f"/events/manage/{event.pk}/delete_participant_type/{participant_type.pk}/").view_name,
            "events:delete_participant_type"
        )

    # TODO: fix - giving 302 instead of 200
    def test_delete_participant_type_url_returns_200_when_event_exists(self):
        generate_addresses()
        generate_serieses()
        generate_locations()
        generate_events()
        generate_users()
        generate_participant_types()
        self.client.force_login(User.objects.get(id=1))
        event = Event.objects.get(pk=1)
        user = User.objects.get(pk=1)
        event.event_staff.set([user])
        event.save()
        participant_type = ParticipantType.objects.get(pk=1)
        kwargs = {
            'event_pk': event.pk,
            'participant_type_pk': participant_type.pk
            }
        url = reverse('events:delete_participant_type', kwargs=kwargs)
        response = self.client.post(url)
        self.assertEqual(HTTPStatus.FOUND, response.status_code) # redirect to event management page
