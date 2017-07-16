from tests.BaseTest import BaseTest
from events.models import Location


class LocationModelTest(BaseTest):

    def test_location(self):
        location = self.event_data.create_location(1)
        query_result = Location.objects.get(slug="location-1")
        self.assertEqual(
            query_result,
            location
        )

    def test_location_slug(self):
        self.event_data.create_location(1)
        query_result = Location.objects.get(slug="location-1")
        self.assertEqual(
            query_result.slug,
            "location-1"
        )

    def test_location_slug_unique(self):
        self.event_data.create_location(1)
        self.event_data.create_location(1)
        self.event_data.create_location(1)
        Location.objects.get(slug="location-1")
        Location.objects.get(slug="location-1-2")
        Location.objects.get(slug="location-1-3")

    def test_location_name(self):
        self.event_data.create_location(1)
        query_result = Location.objects.get(slug="location-1")
        self.assertEqual(
            query_result.name,
            "Location 1"
        )

    def test_location_description(self):
        self.event_data.create_location(1)
        query_result = Location.objects.get(slug="location-1")
        self.assertEqual(
            query_result.description,
            "Description for Location 1"
        )

    def test_location_absolute_url(self):
        self.event_data.create_location(1)
        query_result = Location.objects.get(slug="location-1")
        self.assertEqual(
            query_result.get_absolute_url(),
            "/events/location/location-1/"
        )

    def test_location_str(self):
        location = self.event_data.create_location(1)
        self.assertEqual(location.__str__(), "Location 1")
