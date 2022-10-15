from django.urls import reverse, resolve
from http import HTTPStatus
from events.models import EventRegistration
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


class DeleteRegistrationViaEventPageURLTest(BaseTestWithDB):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_valid_delete_registration_via_event_page_view_url(self):
        generate_addresses()
        generate_serieses()
        generate_locations()
        generate_events()
        generate_users()
        generate_event_registrations()
        registration = EventRegistration.objects.get(pk=1)
        kwargs = {
            'pk': registration.pk,
            }
        url = reverse('events:delete_registration_via_event_page_view', kwargs=kwargs)
        expected_url = f"/events/delete-via-event/{registration.pk}/"
        self.assertEqual(url, expected_url)

    def test_delete_registration_via_registration_page_view_resolve_provides_correct_view_name(self):
        generate_addresses()
        generate_serieses()
        generate_locations()
        generate_events()
        generate_users()
        generate_event_registrations()
        registration = EventRegistration.objects.get(pk=1)
        self.assertEqual(
            resolve(f"/events/delete-via-event/{registration.pk}/").view_name,
            "events:delete_registration_via_event_page_view"
        )

    # TODO: fix - giving 302 instead of 200
    def test_delete_registration_via_event_page_view_url_returns_200_when_event_exists(self):
        generate_addresses()
        generate_serieses()
        generate_locations()
        generate_events()
        generate_users()
        generate_event_registrations()
        self.client.force_login(User.objects.get(id=1))
        registration = EventRegistration.objects.get(pk=1)
        kwargs = {
            'pk': registration.pk,
            }
        url = reverse('events:delete_registration_via_event_page_view', kwargs=kwargs)
        response = self.client.post(url)
        self.assertEqual(HTTPStatus.OK, response.status_code)
