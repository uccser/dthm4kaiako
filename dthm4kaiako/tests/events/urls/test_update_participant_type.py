"""Unit tests for upcoming_participant_type url"""

from django.urls import reverse, resolve
from events.models import Event, ParticipantType
from tests.BaseTestWithDB import BaseTestWithDB
import datetime


class UpdateParticipantTypeURLTest(BaseTestWithDB):

    @classmethod
    def tearDownTestData(cls):
        Event.objects.all().delete()
        ParticipantType.objects.all().delete()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_valid_update_participant_type_url(self):

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
        participant_type = ParticipantType.objects.create(name="Teacher", price="10.00")
        event.participant_types.set([participant_type])
        kwargs = {
            'event_pk': event.pk,
            'participant_type_pk': participant_type.pk
            }
        url = reverse('events:update_participant_type', kwargs=kwargs)
        expected_url = f"/events/manage/{event.pk}/update_participant_type/{participant_type.pk}/"
        self.assertEqual(url, expected_url)

    def test_update_participant_type_resolve_provides_correct_view_name(self):

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
        participant_type = ParticipantType.objects.create(name="Teacher", price="10.00")
        event.participant_types.set([participant_type])
        self.assertEqual(
            resolve(f"/events/manage/{event.pk}/update_participant_type/{participant_type.pk}/").view_name,
            "events:update_participant_type"
        )
