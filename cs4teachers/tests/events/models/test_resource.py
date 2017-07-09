from tests.BaseTest import BaseTest
from events.models import Resource


class ResourceModelTest(BaseTest):

    def test_resource(self):
        resource = self.event_data.create_resource(1)
        query_result = Resource.objects.get(slug="resource-1")
        self.assertEqual(
            query_result,
            resource
        )

    def test_resource_slug(self):
        self.event_data.create_resource(1)
        query_result = Resource.objects.get(slug="resource-1")
        self.assertEqual(
            query_result.slug,
            "resource-1"
        )

    def test_resource_slug_unique(self):
        self.event_data.create_resource(1)
        self.event_data.create_resource(1)
        self.event_data.create_resource(1)
        Resource.objects.get(slug="resource-1")
        Resource.objects.get(slug="resource-1-2")
        Resource.objects.get(slug="resource-1-3")

    def test_resource_name(self):
        self.event_data.create_resource(1)
        query_result = Resource.objects.get(slug="resource-1")
        self.assertEqual(
            query_result.name,
            "Resource 1"
        )

    def test_resource_url(self):
        self.event_data.create_resource(1)
        query_result = Resource.objects.get(slug="resource-1")
        self.assertEqual(
            query_result.url,
            "https://www.1.com/"
        )

    def test_resource_description(self):
        self.event_data.create_resource(1)
        query_result = Resource.objects.get(slug="resource-1")
        self.assertEqual(
            query_result.description,
            "Description for Resource 1"
        )

    def test_resource_str(self):
        resource = self.event_data.create_resource(1)
        self.assertEqual(resource.__str__(), "Resource 1")
