from django.urls import reverse, resolve
from http import HTTPStatus
from tests.BaseTestWithDB import BaseTestWithDB
from users.models import User
from events.models import Event

class RegistrationsURLTest(BaseTestWithDB):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_valid_registrations_url(self):
        url = reverse("events:event_registrations")
        self.assertEqual(url, "/events/registrations/")

    def test_registrations_resolve_provides_correct_view_name(self):
        self.assertEqual(resolve("/events/registrations/").view_name, "events:event_registrations")

    # TODO: fix me - giving 302 instead of 200
    def test_registrations_gives_200_status_code(self):
        event = Event.objects.get(pk=1)
        user = User.objects.get(pk=1)
        event.event_staff.set([user])
        event.save()
        self.client.force_login(user)
        url = reverse("events:event_registrations")
        response = self.client.post(url)
        self.assertEqual(HTTPStatus.OK, response.status_code)
