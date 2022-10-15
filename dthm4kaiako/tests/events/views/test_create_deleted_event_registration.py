"""Unit tests for delete_registration_via_event_page_view"""

from django.urls import reverse, resolve
from http import HTTPStatus
from events.models import (
    EventRegistration,
    Event,
    ParticipantType,
    Address,
    DeletedEventRegistration
)
from tests.BaseTestWithDB import BaseTestWithDB
from users.models import User
import datetime
from events.views import create_deleted_event_registration
from django.test.client import RequestFactory


class CreateDeletedEventRegistrationTest(BaseTestWithDB):

    @classmethod
    def tearDownTestData(cls):
        EventRegistration.objects.all().delete()
        Event.objects.all().delete()
        ParticipantType.objects.all().delete()
        Address.objects.all().delete()
        DeletedEventRegistration.objects.all().delete()

    def test_created_deleted_registration_successfully_and_no_other_reason(self):
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

        count_prior = DeletedEventRegistration.objects.filter(event=event, withdraw_reason="1").count()

        kwargs = {
            'pk': event_registration.pk,
            }
        url = reverse('events:delete_registration_via_event_page_view', kwargs=kwargs)

        self.factory = RequestFactory()
        request = self.factory.post(url, {"withdraw_reason": "1", "other_reason_for_withdrawing": ""})
        create_deleted_event_registration(event, request)
        self.assertEqual(DeletedEventRegistration.objects.filter(event=event, withdraw_reason="1").count(), count_prior + 1)

    def test_created_deleted_registration_successfully_and_no_other_reason(self):
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

        count_prior = DeletedEventRegistration.objects.filter(event=event, withdraw_reason="1", other_reason_for_withdrawing="Another reason").count()

        kwargs = {
            'pk': event_registration.pk,
            }
        url = reverse('events:delete_registration_via_event_page_view', kwargs=kwargs)

        self.factory = RequestFactory()
        request = self.factory.post(url, {"withdraw_reason": "1", "other_reason_for_withdrawing": "Another reason"})
        create_deleted_event_registration(event, request)
        self.assertEqual(DeletedEventRegistration.objects.filter(event=event, withdraw_reason="1", other_reason_for_withdrawing="Another reason").count(), count_prior + 1)
