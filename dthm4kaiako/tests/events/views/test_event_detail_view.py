"""Unit tests for does_registration_exist"""

from tests.BaseTestWithDB import BaseTestWithDB
from django.urls import reverse
from http import HTTPStatus
from django.test.utils import override_settings
import datetime
import pytz
from events.models import (
    EventRegistration,
    Event,
    ParticipantType,
    Address
)
from users.models import User
from events.views import EventDetailView
from django.test import RequestFactory

NEW_ZEALAND_TIME_ZONE = pytz.timezone('Pacific/Auckland')


def setup_view(view, request, *args, **kwargs):
    """
    Mimic ``as_view()``, but returns view instance.
    Use this function to get view instances on which you can run unit tests,
    by testing specific methods.
    """

    view.request = request
    view.args = args
    view.kwargs = kwargs
    return view


class EventDetailViewTest(BaseTestWithDB):

    @classmethod
    def tearDownTestData(cls):
        EventRegistration.objects.all().delete()
        Event.objects.all().delete()
        ParticipantType.objects.all().delete()
        Address.objects.all().delete()
        User.objects.all().delete()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @override_settings(GOOGLE_MAPS_API_KEY="mocked")
    def test_event_detail_view_success_response(self):
        kwargs = {'pk': 1}
        response = self.client.get(reverse("events:register", kwargs=kwargs))
        self.assertEqual(HTTPStatus.FOUND, response.status_code)

    # ------------------------------ tests for does_registration_exist_provided_logged_in -------------------------

    def test_does_registration_exist_provided_logged_in_when_exists_and_logged_in_returns_true(self):
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
            username='kate',
            first_name='Kate',
            last_name='Bush',
            email='kate@uclive.ac.nz',
            password='potato',
        )
        user.save()
        self.client.force_login(user)

        participant_type = ParticipantType.objects.create(name="Teacher", price="10.00")

        billing_address = Address.objects.create(
            id=1,
            street_number='12',
            street_name='High Street',
            suburb='Riccarton',
            city='Chrirstchurch',
            region=14
        )
        billing_address.save()

        event_registration = EventRegistration.objects.create(
            participant_type=participant_type,
            user=user,
            event=event,
            billing_physical_address=billing_address,
            billing_email_address="test@test.co.nz"
        )
        event_registration.status = 1
        event_registration.save()

        factory = RequestFactory()
        request = factory.get(f'/events/event/{event.pk}/')
        view = setup_view(EventDetailView(), request)
        view.object = event
        self.assertTrue(view.does_registration_exist_provided_logged_in(user))

    def test_does_registration_exist_provided_logged_in_when_does_not_exist_and_logged_in_returns_false(self):
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
            username='kate',
            first_name='Kate',
            last_name='Bush',
            email='kate@uclive.ac.nz',
            password='potato',
        )
        user.save()
        self.client.force_login(user)

        factory = RequestFactory()
        request = factory.get(f'/events/event/{event.pk}/')
        view = setup_view(EventDetailView(), request)
        view.object = event
        self.assertFalse(view.does_registration_exist_provided_logged_in(user))

    def test_does_registration_exist_provided_logged_in_when_does_not_exist_and_not_logged_in_returns_false(self):
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
            username='kate',
            first_name='Kate',
            last_name='Bush',
            email='kate@uclive.ac.nz',
            password='potato',
        )
        user.save()

        factory = RequestFactory()
        request = factory.get(f'/events/event/{event.pk}/')
        view = setup_view(EventDetailView(), request)
        view.object = event
        self.assertFalse(view.does_registration_exist_provided_logged_in(user))
