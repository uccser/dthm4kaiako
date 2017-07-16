from tests.BaseTest import BaseTest
from events.models import ThirdPartyEvent


class ThirdPartyEventModelTest(BaseTest):

    def setUp(self, *args, **kwargs):
        self.location = self.event_data.create_location(1)

    def test_third_party_event(self):
        third_party_event = self.event_data.create_third_party_event(1, location=self.location)
        query_result = ThirdPartyEvent.objects.get(slug="third-party-event-1")
        self.assertEqual(
            query_result,
            third_party_event
        )

    def test_third_party_event_slug(self):
        self.event_data.create_third_party_event(1, location=self.location)
        query_result = ThirdPartyEvent.objects.get(slug="third-party-event-1")
        self.assertEqual(
            query_result.slug,
            "third-party-event-1"
        )

    def test_third_party_event_slug_unique(self):
        self.event_data.create_third_party_event(1, location=self.location)
        self.event_data.create_third_party_event(1, location=self.location)
        self.event_data.create_third_party_event(1, location=self.location)
        ThirdPartyEvent.objects.get(slug="third-party-event-1")
        ThirdPartyEvent.objects.get(slug="third-party-event-1-2")
        ThirdPartyEvent.objects.get(slug="third-party-event-1-3")
