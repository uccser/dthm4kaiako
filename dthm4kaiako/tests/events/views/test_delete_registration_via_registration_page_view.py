"""Unit tests for delete_registration_via_registration_page_view"""

from django.urls import reverse
from http import HTTPStatus
from events.models import (
    EventRegistration,
    Event,
    ParticipantType,
    Address
)
from tests.BaseTestWithDB import BaseTestWithDB
from users.models import User
import datetime


class DeletingRegistrationViaRegistrationsViewTest(BaseTestWithDB):

    @classmethod
    def tearDownTestData(cls):
        EventRegistration.objects.all().delete()
        Event.objects.all().delete()
        ParticipantType.objects.all().delete()
        Address.objects.all().delete()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_delete_registration_via_registration_page_view_url_returns_200_when_event_exists(self):
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
        kwargs = {
            'pk': event_registration.pk,
            }
        url = reverse('events:delete_registration_via_registration_page_view', kwargs=kwargs)
        response = self.client.post(url, {"withdraw_reason": "1", "other_reason_for_withdrawing": ""})
        self.assertEqual(HTTPStatus.FOUND, response.status_code)
        self.assertEqual(response['Location'], '/events/registrations/')

    def test_delete_registration_via_registration_page_and_logged_in_and_mine_then_successfully_deleted(self):
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
        kwargs = {
            'pk': event_registration.pk,
            }
        url = reverse('events:delete_registration_via_registration_page_view', kwargs=kwargs)
        self.client.post(url, {"withdraw_reason": "1", "other_reason_for_withdrawing": ""})
        self.assertQuerysetEqual(
            EventRegistration.objects.filter(event=event, user=user),
            EventRegistration.objects.none()
        )

    def test_delete_registration_via_registration_page_and_not_logged_in_and_mine_then_redirected(self):
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
        kwargs = {
            'pk': event_registration.pk,
            }
        url = reverse('events:delete_registration_via_registration_page_view', kwargs=kwargs)
        response = self.client.post(url, {"withdraw_reason": "1", "other_reason_for_withdrawing": ""})
        self.assertEqual(HTTPStatus.FOUND, response.status_code)
        self.assertEqual(
            response['Location'],
            f'/accounts/login/?next=/events/delete-via-registrations/{event_registration.pk}/'
        )

    def test_delete_registration_via_registration_page_and_logged_in_and_not_mine_then_redirected(self):
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
        user_2 = User.objects.create_user(
            username='Bob',
            first_name='Bob',
            last_name='Bush',
            email='bob@uclive.ac.nz',
            password='carrot',
        )
        user_2.save()
        self.client.force_login(user_2)

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
        kwargs = {
            'pk': event_registration.pk,
            }
        url = reverse('events:delete_registration_via_registration_page_view', kwargs=kwargs)
        response = self.client.post(url, {"withdraw_reason": "1", "other_reason_for_withdrawing": ""})
        self.assertEqual(HTTPStatus.FOUND, response.status_code)
        self.assertEqual(response['Location'], '/events/registrations/')
