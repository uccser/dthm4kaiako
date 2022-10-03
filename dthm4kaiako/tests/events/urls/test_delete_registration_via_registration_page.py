from django.urls import reverse, resolve
from http import HTTPStatus
from events.models import Event, EventRegistration, ParticipantType
from users.models import User
from tests.dthm4kaiako_test_data_generator import (
    generate_locations,
    generate_users,
    generate_events,
    generate_addresses,
    generate_serieses,
)
from tests.BaseTestWithDB import BaseTestWithDB


class DeleteRegistrationViaRegistrationPageURLTest(BaseTestWithDB):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_valid_delete_registration_via_registration_page_url(self):
        generate_addresses()
        generate_serieses()
        generate_locations()
        generate_events()
        generate_users()
        event = Event.objects.get(pk=1)
        participant_type_free_event_staff = ParticipantType.objects.create(name="Event Staff", price=0.0)
        registration = EventRegistration.objects.create(
            participant_type=participant_type_free_event_staff,
            user=User.objects.get(pk=1),
            representing="myself",
            event=event
        )
        kwargs = {
            'pk': registration.pk,
            }
        url = reverse('events:delete_registration_via_registration_page', kwargs=kwargs)
        expected_url = f"/events/delete-via-registrations/{registration.pk}/"
        self.assertEqual(url, expected_url)

    def test_delete_registration_via_registration_page_resolve_provides_correct_view_name(self):
        generate_addresses()
        generate_serieses()
        generate_locations()
        generate_events()
        generate_users()
        event = Event.objects.get(pk=1)
        participant_type_free_event_staff = ParticipantType.objects.create(name="Event Staff", price=0.0)
        registration = EventRegistration.objects.create(
            participant_type=participant_type_free_event_staff,
            user=User.objects.get(pk=1),
            representing="myself",
            event=event
        )
        self.assertEqual(resolve(f"/events/delete-via-registrations/{registration.pk}/").view_name, "events:delete_registration_via_registration_page")

    # TODO: fix - giving 302 instead of 200
    def test_delete_registration_via_registration_page_returns_200_when_registration_exists(self):
        generate_addresses()
        generate_serieses()
        generate_locations()
        generate_events()
        generate_users()
        self.client.login(id=1, password='password')
        event = Event.objects.get(pk=1)
        participant_type_free_event_staff = ParticipantType.objects.create(name="Event Staff", price=0.0)
        registration = EventRegistration.objects.create(
            participant_type=participant_type_free_event_staff,
            user=User.objects.get(pk=1),
            representing="myself",
            event=event
        )
        kwargs = {
            'pk': registration.pk,
            }
        url = reverse('events:delete_registration_via_registration_page', kwargs=kwargs)
        response = self.client.get(url)
        self.assertEqual(HTTPStatus.OK, response.status_code)
