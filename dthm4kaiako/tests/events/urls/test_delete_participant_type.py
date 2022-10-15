"""Unit tests for delete_participant_type url"""

from django.urls import reverse, resolve
from events.models import Event, ParticipantType
from tests.BaseTestWithDB import BaseTestWithDB
from users.models import User
import datetime


class DeleteParticipantTypeURLTest(BaseTestWithDB):

    
    @classmethod
    def tearDownTestData(cls):
        Event.objects.all().delete()
        ParticipantType.objects.all().delete()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_valid_delete_participant_type_url(self):
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
        expected_url = f"/events/manage/{event.pk}/delete_participant_type/{participant_type.pk}/"
        self.assertEqual(url, expected_url)

    def test_delete_participant_type_resolve_provides_correct_view_name(self):
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
        self.assertEqual(
            resolve(f"/events/manage/{event.pk}/delete_participant_type/{participant_type.pk}/").view_name,
            "events:delete_participant_type"
        )
