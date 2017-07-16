from tests.BaseTest import BaseTest
from events.models import Event


class EventModelTest(BaseTest):

    def setUp(self, *args, **kwargs):
        self.location = self.event_data.create_location(1)

    def test_event(self):
        event = self.event_data.create_event(1, location=self.location)
        query_result = Event.objects.get(slug="event-1")
        self.assertEqual(
            query_result,
            event
        )

    def test_event_slug(self):
        self.event_data.create_event(1, location=self.location)
        query_result = Event.objects.get(slug="event-1")
        self.assertEqual(
            query_result.slug,
            "event-1"
        )

    def test_event_with_series_slug(self):
        series = self.event_data.create_series(1)
        self.event_data.create_event(1, series=series, location=self.location)
        query_result = Event.objects.get(slug="series-1-event-1")
        self.assertEqual(
            query_result.slug,
            "series-1-event-1"
        )

    def test_event_slug_unique(self):
        self.event_data.create_event(1, location=self.location)
        self.event_data.create_event(1, location=self.location)
        self.event_data.create_event(1, location=self.location)
        Event.objects.get(slug="event-1")
        Event.objects.get(slug="event-1-2")
        Event.objects.get(slug="event-1-3")


    def test_event_with_series_slug_unique(self):
        series = self.event_data.create_series(1)
        self.event_data.create_event(1, series=series, location=self.location)
        self.event_data.create_event(1, series=series, location=self.location)
        self.event_data.create_event(1, series=series, location=self.location)
        Event.objects.get(slug="series-1-event-1")
        Event.objects.get(slug="series-1-event-1-2")
        Event.objects.get(slug="series-1-event-1-3")
