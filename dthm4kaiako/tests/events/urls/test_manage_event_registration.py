"""Unit tests for manage_event_registration url"""

from django.urls import reverse, resolve
from http import HTTPStatus
from events.models import (
    Event,
    EventRegistration,
    ParticipantType,
    Address,
)
from users.models import User
from tests.BaseTestWithDB import BaseTestWithDB
from users.models import User
from django.test.utils import override_settings
import datetime


class ManageEventRegistrationURLTest(BaseTestWithDB):

    @classmethod
    def tearDownTestData(cls):
        EventRegistration.objects.all().delete()
        Event.objects.all().delete()
        ParticipantType.objects.all().delete()
        Address.objects.all().delete()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_valid_manage_event_registration_url(self):
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
            participant_type= participant_type,
            user=user,
            event=event,
            billing_physical_address=billing_address,
            billing_email_address="test@test.co.nz"
        )
        event_registration.status = 1
        event_registration.save()
        kwargs = {
            'pk_event': event.pk,
            'pk_registration': event_registration.pk
            }
        url = reverse('events:manage_event_registration', kwargs=kwargs)
        expected_url = f"/events/event/{event.pk}/manage-event-registration/{event_registration.pk}/"
        self.assertEqual(url, expected_url)

    def test_manage_event_registration_resolve_provides_correct_view_name(self):
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
            participant_type= participant_type,
            user=user,
            event=event,
            billing_physical_address=billing_address,
            billing_email_address="test@test.co.nz"
        )
        event_registration.status = 1
        event_registration.save()
        self.assertEqual(
            resolve(f"/events/event/{event.pk}/manage-event-registration/{event_registration.pk}/").view_name,
            "events:manage_event_registration"
        )
