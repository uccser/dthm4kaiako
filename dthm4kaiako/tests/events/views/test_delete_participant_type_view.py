"""Unit tests for delete_participant_type_view"""

from django.urls import reverse
from http import HTTPStatus
from events.models import Event, ParticipantType
from tests.BaseTestWithDB import BaseTestWithDB
from users.models import User
import datetime

class DeleteParticipantTypeURLTest(BaseTestWithDB):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    
    def test_delete_participant_type_view_returns_200_when_event_exists_and_logged_in_and_staff(self):
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
        event.event_staff.set([user])
        event.save()
        self.client.force_login(user)
        participant_type = ParticipantType.objects.create(name="Teacher", price="10.00")
        kwargs = {
            'event_pk': event.pk,
            'participant_type_pk': participant_type.pk
            }
        url = reverse('events:delete_participant_type', kwargs=kwargs)
        response = self.client.post(url)
        self.assertEqual(HTTPStatus.FOUND, response.status_code) # redirect to event management page
        self.assertEqual(response['Location'], f'/events/manage/{event.pk}/')

    def test_delete_participant_type_view_and_logged_in_and_staff_and_successfully_deletes_participant_type_when_it_only_belongs_to_this_event(self):
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
        event.event_staff.set([user])
        event.save()
        self.client.force_login(user)
        participant_type = ParticipantType.objects.create(name="Teacher", price="10.00")
        event.participant_types.set([participant_type])
        kwargs = {
            'event_pk': event.pk,
            'participant_type_pk': participant_type.pk
            }
        url = reverse('events:delete_participant_type', kwargs=kwargs)
        self.client.post(url)
        self.assertEqual(ParticipantType.objects.filter(name="Teacher", price="10.00").count(), 0)

    def test_delete_participant_type_view_and_logged_in_and_staff_and_successfully_removes_participant_from_event_when_belongs_to_other_events_too(self):
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
        event_2 = Event.objects.create(
            name="Security in CS (Advanced)",
            description="description",
            registration_type=2,
            start=datetime.datetime(2023, 2, 13),
            end=datetime.datetime(2023, 2, 14),
            accessible_online=False,
            published=True
        )
        event_2.save()
        user = User.objects.create_user(
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
        participant_type = ParticipantType.objects.create(name="Teacher", price="10.00")
        event.participant_types.set([participant_type])
        event_2.participant_types.set([participant_type])
        kwargs = {
            'event_pk': event.pk,
            'participant_type_pk': participant_type.pk
            }
        url = reverse('events:delete_participant_type', kwargs=kwargs)
        self.client.post(url)
        self.assertEqual(ParticipantType.objects.filter(name="Teacher", price="10.00").count(), 1)
        self.assertQuerysetEqual(event.participant_types.all(), ParticipantType.objects.none())
        event_2_expected_queryset = ParticipantType.objects.filter(name="Teacher", price="10.00")
        self.assertQuerysetEqual(event_2.participant_types.all(), event_2_expected_queryset)


    def test_delete_participant_type_view_and_not_logged_in(self):
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
        participant_type = ParticipantType.objects.create(name="Teacher", price="10.00")
        kwargs = {
            'event_pk': event.pk,
            'participant_type_pk': participant_type.pk
            }
        url = reverse('events:delete_participant_type', kwargs=kwargs)
        response = self.client.post(url)
        self.assertEqual(HTTPStatus.FOUND, response.status_code) # redirect to event management page
        self.assertEqual(response['Location'], f'/accounts/login/?next=/events/manage/{event.pk}/delete_participant_type/{participant_type.pk}/')

    def test_delete_participant_type_view_and_logged_in_and_not_staff(self):
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
        event.save()
        participant_type = ParticipantType.objects.create(name="Teacher", price="10.00")
        kwargs = {
            'event_pk': event.pk,
            'participant_type_pk': participant_type.pk
            }
        url = reverse('events:delete_participant_type', kwargs=kwargs)
        response = self.client.post(url)
        self.assertEqual(HTTPStatus.FOUND, response.status_code) # redirect to event management page
        self.assertEqual(response['Location'], f'/events/manage/')