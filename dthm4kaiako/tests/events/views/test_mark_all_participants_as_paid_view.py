"""Unit tests for mark_all_participants_as_paid_view"""

from django.urls import reverse
from http import HTTPStatus
from events.models import (
    Event,
    ParticipantType,
    Address,
    EventRegistration
)
from users.models import User
from tests.BaseTestWithDB import BaseTestWithDB
from users.models import User
import datetime


class MarkAllParticipantsAsPaidViewTest(BaseTestWithDB):

    @classmethod
    def tearDownTestData(cls):
        Event.objects.all().delete()
        ParticipantType.objects.all().delete()
        Address.objects.all().delete()
        EventRegistration.objects.all().delete()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_mark_all_participants_as_paid_url_returns_200_when_event_exists(self):
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
        self.client.force_login(user)
        event.event_staff.set([user])
        event.save()

        kwargs = {
            'pk': event.pk,
            }
        url = reverse('events:mark_all_participants_as_paid', kwargs=kwargs)
        response = self.client.post(url)
        self.assertEqual(HTTPStatus.FOUND, response.status_code) # redirect to event management page
        self.assertEqual(response['Location'], f'/events/manage/{event.pk}/')

    # TODO
    def test_mark_all_participants_as_paid_view_and_logged_in_and_staff_and_successfully_updates(self):
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
            participant_type= participant_type,
            user=user,
            event=event,
            billing_physical_address=billing_address,
            billing_email_address="test@test.co.nz",
            paid=False
        )
        event_registration.status = 1
        event_registration.save()

        self.client.force_login(user)
        event.event_staff.set([user])
        event.save()

        self.client.force_login(user)
        kwargs = {
            'pk': event.pk,
            }
        url = reverse('events:mark_all_participants_as_paid', kwargs=kwargs)
        self.client.post(url)
        updated_event_registration = EventRegistration.objects.get(pk=event_registration.pk)
        self.assertTrue(updated_event_registration.paid)

    
    def test_mark_all_participants_as_paid_view_and_not_logged_in_and_staff_and_redirects(self):
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
            participant_type= participant_type,
            user=user,
            event=event,
            billing_physical_address=billing_address,
            billing_email_address="test@test.co.nz"
        )
        event_registration.status = 1
        event_registration.save()

        event.event_staff.set([user])
        event.save()
        kwargs = {
            'pk': event.pk,
            }
        url = reverse('events:mark_all_participants_as_paid', kwargs=kwargs)
        response = self.client.post(url)
        self.assertEqual(HTTPStatus.FOUND, response.status_code) # redirect to event management page
        self.assertEqual(response['Location'], f'/accounts/login/?next=/events/manage/mark_all_participants_as_paid/{event.pk}/')

    def test_mark_all_participants_as_paid_view_and_logged_in_and_not_staff_and_redirects(self):
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
            participant_type= participant_type,
            user=user,
            event=event,
            billing_physical_address=billing_address,
            billing_email_address="test@test.co.nz"
        )
        event_registration.status = 1
        event_registration.save()

        self.client.force_login(user)
        kwargs = {
            'pk': event.pk,
            }
        url = reverse('events:mark_all_participants_as_paid', kwargs=kwargs)
        response = self.client.post(url)
        self.assertEqual(HTTPStatus.FOUND, response.status_code) # redirect to event management page
        self.assertEqual(response['Location'], f'/events/manage/')