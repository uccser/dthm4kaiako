from tests.BaseTest import BaseTest
from events.models import Event


class EventModelTest(BaseTest):

    def setUp(self, *args, **kwargs):
        self.location = self.event_data.create_location(1)

    def test_event(self):
        event = self.event_data.create_event(1, self.location)
        query_result = Event.objects.get(slug="event-1")
        self.assertEqual(
            query_result,
            event
        )

    def test_event_slug(self):
        self.event_data.create_event(1, self.location)
        query_result = Event.objects.get(slug="event-1")
        self.assertEqual(
            query_result.slug,
            "event-1"
        )

    def test_event_slug_unique(self):
        event_a = self.event_data.create_event(1, self.location)
        event_b = self.event_data.create_event(1, self.location)
        event_c = self.event_data.create_event(1, self.location)
        query_result = Event.objects.get(slug="event-1")
        query_result = Event.objects.get(slug="event-1-2")
        query_result = Event.objects.get(slug="event-1-3")
