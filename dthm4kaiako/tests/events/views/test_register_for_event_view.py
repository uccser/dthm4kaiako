from tests.BaseTestWithDB import BaseTestWithDB
from django.urls import reverse
from http import HTTPStatus
from django.test.utils import override_settings
from users.models import User
from events.models import (
    Event,
)
import datetime
import pytz
NEW_ZEALAND_TIME_ZONE = pytz.timezone('Pacific/Auckland')


class ApplyForEventViewTest(BaseTestWithDB):

    @classmethod
    def tearDownTestData(cls):
        Event.objects.all().delete()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.language = "en"

    @override_settings(GOOGLE_MAPS_API_KEY="mocked")
    def test_register_for_event_view_view_when_not_logged_in_redirect_response(self):
        kwargs = {'pk': 1}
        response = self.client.get(reverse("events:register", kwargs=kwargs))
        self.assertEqual(HTTPStatus.FOUND, response.status_code)

    @override_settings(GOOGLE_MAPS_API_KEY="mocked")
    def test_register_returns_200_when_event_exists_and_logged_in(self):
        event = Event.objects.create(
            name="Security in CS",
            description="description",
            registration_type=2,
            start=datetime.datetime(2023, 2, 13),
            end=datetime.datetime(2023, 2, 14),
            accessible_online=False,
            published=True
        )
        event.save()
        user = User.objects.create_user(
            id=1,
            username='kate',
            first_name='Kate',
            last_name='Bush',
            email='kate@uclive.ac.nz',
            password='potato',
        )
        user.save()
        event.event_staff.set([user])
        event.save()
        self.client.force_login(user)
        kwargs = {
            'pk': event.pk,
            }
        url = reverse('events:register', kwargs=kwargs)
        response = self.client.post(url)
        self.assertEqual(HTTPStatus.OK, response.status_code)

    #TODO: write test - need to mock post request body
    @override_settings(GOOGLE_MAPS_API_KEY="mocked")
    def test_register_successfully_for_free_event(self):
        pass 

    #TODO: write test - need to mock post request body
    @override_settings(GOOGLE_MAPS_API_KEY="mocked")
    def test_register_successfully_for_paid_event(self):
        pass 
    
    #TODO: write test - need to mock post request body
    @override_settings(GOOGLE_MAPS_API_KEY="mocked")
    def test_register_successfully_for_online_event(self):
        pass 

    #TODO: write test - need to mock post request body
    @override_settings(GOOGLE_MAPS_API_KEY="mocked")
    def test_register_successfully_for_in_person_event(self):
        pass 

    #TODO: write test - need to mock post request body
    @override_settings(GOOGLE_MAPS_API_KEY="mocked")
    def test_register_successfully_for_in_person_catered_event(self):
        pass
