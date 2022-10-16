"""Unit tests for manage_event_registration_form_details url"""

from django.urls import reverse, resolve
import datetime
from events.models import (
    Event,
)
import pytz
from tests.BaseTestWithDB import BaseTestWithDB
from users.models import User
NEW_ZEALAND_TIME_ZONE = pytz.timezone('Pacific/Auckland')


class ManageEventRegistrationFormDetailsURLTest(BaseTestWithDB):

    @classmethod
    def tearDownTestData(cls):
        Event.objects.all().delete()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_valid_manage_event_registration_form_details_url(self):
        event = Event.objects.create(
            id=1,
            name="DTHM for Kaiako Conference 2023",
            description="description",
            registration_type=1,
            start=datetime.datetime(2023, 6, 24, 0, 0, 0, 00, NEW_ZEALAND_TIME_ZONE),
            end=datetime.datetime(2023, 6, 26, 0, 0, 0, 00, NEW_ZEALAND_TIME_ZONE),
            accessible_online=False,
            published=True
        )
        event.save()
        kwargs = {
            'pk': event.pk,
            }
        url = reverse('events:manage_event_registration_form_details', kwargs=kwargs)
        expected_url = f"/events/manage-event-registration-form-details/{event.pk}/"
        self.assertEqual(url, expected_url)

    def test_manage_event_registration_form_details_resolve_provides_correct_view_name(self):
        event = Event.objects.create(
            id=1,
            name="DTHM for Kaiako Conference 2023",
            description="description",
            registration_type=1,
            start=datetime.datetime(2023, 6, 24, 0, 0, 0, 00, NEW_ZEALAND_TIME_ZONE),
            end=datetime.datetime(2023, 6, 26, 0, 0, 0, 00, NEW_ZEALAND_TIME_ZONE),
            accessible_online=False,
            published=True
        )
        event.save()
        self.assertEqual(resolve(
            f"/events/manage-event-registration-form-details/{event.pk}/").view_name,
            "events:manage_event_registration_form_details"
        )

