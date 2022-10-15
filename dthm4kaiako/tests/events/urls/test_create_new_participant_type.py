from django.urls import reverse, resolve
from events.models import Event
from users.models import User
from tests.BaseTestWithDB import BaseTestWithDB
import datetime


class CreateNewParticipantTypeURLTest(BaseTestWithDB):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_valid_create_new_participant_type_url(self):
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
        kwargs = {
            'pk': event.pk,
            }
        url = reverse('events:create_new_participant_type', kwargs=kwargs)
        expected_url = f"/events/manage/create_new_participant_type/{event.pk}/"
        self.assertEqual(url, expected_url)

    def test_create_new_participant_type_resolve_provides_correct_view_name(self):
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
        self.assertEqual(resolve(
            f"/events/manage/create_new_participant_type/{event.pk}/").view_name,
            "events:create_new_participant_type"
        )
