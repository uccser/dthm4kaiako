"""Unit tests for delete_registration_via_event_page_view url"""

from django.urls import reverse, resolve
from events.models import (
    EventRegistration,
    Event,
    ParticipantType,
    Address,
)
from tests.BaseTestWithDB import BaseTestWithDB
from users.models import User
import datetime


class DeleteRegistrationViaEventPageURLTest(BaseTestWithDB):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_valid_delete_registration_via_event_page_view_url(self):
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
            'pk': event_registration.pk,
            }
        url = reverse('events:delete_registration_via_event_page_view', kwargs=kwargs)
        expected_url = f"/events/delete-via-event/{event_registration.pk}/"
        self.assertEqual(url, expected_url)

    def test_delete_registration_via_event_page_view_resolve_provides_correct_view_name(self):
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
            resolve(f"/events/delete-via-event/{event_registration.pk}/").view_name,
            "events:delete_registration_via_event_page_view"
        )
