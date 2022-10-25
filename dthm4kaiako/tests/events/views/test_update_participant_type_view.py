"""Unit tests for upcoming_participant_type_view"""

from django.urls import reverse
from http import HTTPStatus
from events.models import Event, ParticipantType
from tests.BaseTestWithDB import BaseTestWithDB
from users.models import User
import datetime
from django.test.client import RequestFactory


class UpdateParticipantTypeViewTest(BaseTestWithDB):

    @classmethod
    def tearDownTestData(cls):
        Event.objects.all().delete()
        ParticipantType.objects.all().delete()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_update_participant_type_view_returns_302_when_event_exists(self):
        user = User.objects.create_user(
            id=1,
            username='kate',
            first_name='Kate',
            last_name='Bush',
            email='kate@uclive.ac.nz',
            password='potato',
        )
        user.save()
        event = Event.objects.create(
            id=1,
            name="DTHM for Kaiako Conference 2023",
            description="description",
            registration_type=1,
            start=datetime.date(2023, 6, 24),
            end=datetime.date(2023, 6, 26),
            accessible_online=False,
            published=True
        )
        event.save()
        event.event_staff.set([user])
        event.save()
        self.client.force_login(user)
        participant_type = ParticipantType.objects.create(name="Teacher", price="10.00")
        participant_type.save()
        event.participant_types.set([participant_type])
        kwargs = {
            'event_pk': event.pk,
            'participant_type_pk': participant_type.pk
            }
        url = reverse('events:update_participant_type', kwargs=kwargs)
        response = self.client.post(url, {'name': "teacher", 'price': "15.0"})
        self.assertEqual(HTTPStatus.FOUND, response.status_code)
        self.assertEqual(response['Location'], f'/events/manage/{event.pk}/')

    def test_update_participant_type_view_and_logged_in_and_staff_then_update_participant_type(self):
        user = User.objects.create_user(
            id=1,
            username='kate',
            first_name='Kate',
            last_name='Bush',
            email='kate@uclive.ac.nz',
            password='potato',
        )
        user.save()
        event = Event.objects.create(
            id=1,
            name="DTHM for Kaiako Conference 2023",
            description="description",
            registration_type=1,
            start=datetime.date(2023, 6, 24),
            end=datetime.date(2023, 6, 26),
            accessible_online=False,
            published=True
        )
        event.save()
        event.event_staff.set([user])
        event.save()
        self.client.force_login(user)
        participant_type = ParticipantType.objects.create(name="Teacher", price="10.00")
        participant_type.save()
        event.participant_types.set([participant_type])
        self.factory = RequestFactory()
        kwargs = {
            'event_pk': event.pk,
            'participant_type_pk': participant_type.pk
            }
        url = reverse('events:update_participant_type', kwargs=kwargs)
        self.client.post(url, {'name': "teacher", 'price': "15.0"})
        self.assertEqual(ParticipantType.objects.last().name, "teacher")

    def test_update_participant_type_view_and_not_logged_in_and_staff_then_redirect(self):
        user = User.objects.create_user(
            id=1,
            username='kate',
            first_name='Kate',
            last_name='Bush',
            email='kate@uclive.ac.nz',
            password='potato',
        )
        user.save()
        event = Event.objects.create(
            id=1,
            name="DTHM for Kaiako Conference 2023",
            description="description",
            registration_type=1,
            start=datetime.date(2023, 6, 24),
            end=datetime.date(2023, 6, 26),
            accessible_online=False,
            published=True
        )
        event.save()
        event.event_staff.set([user])
        event.save()
        participant_type = ParticipantType.objects.create(name="Teacher", price="10.00")
        participant_type.save()
        event.participant_types.set([participant_type])
        kwargs = {
            'event_pk': event.pk,
            'participant_type_pk': participant_type.pk
            }
        url = reverse('events:update_participant_type', kwargs=kwargs)
        response = self.client.post(url)
        self.assertEqual(HTTPStatus.FOUND, response.status_code)
        self.assertEqual(
            response['Location'],
            f'/accounts/login/?next=/events/manage/{event.pk}/update_participant_type/{participant_type.pk}/'
        )

    def test_update_participant_type_view_and_logged_in_and_not_staff_then_redirect(self):
        user = User.objects.create_user(
            id=1,
            username='kate',
            first_name='Kate',
            last_name='Bush',
            email='kate@uclive.ac.nz',
            password='potato',
        )
        user.save()
        event = Event.objects.create(
            id=1,
            name="DTHM for Kaiako Conference 2023",
            description="description",
            registration_type=1,
            start=datetime.date(2023, 6, 24),
            end=datetime.date(2023, 6, 26),
            accessible_online=False,
            published=True
        )
        event.save()
        self.client.force_login(user)
        participant_type = ParticipantType.objects.create(name="Teacher", price="10.00")
        participant_type.save()
        event.participant_types.set([participant_type])
        kwargs = {
            'event_pk': event.pk,
            'participant_type_pk': participant_type.pk
            }
        url = reverse('events:update_participant_type', kwargs=kwargs)
        response = self.client.post(url)
        self.assertEqual(HTTPStatus.FOUND, response.status_code)
        self.assertEqual(response['Location'], '/events/manage/')
