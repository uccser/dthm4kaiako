from django.test import TestCase
from django.urls import reverse


class IndexURLTest(TestCase):

    def test_valid_index_request(self):
        url = reverse("general:home")
        self.assertEqual(url, "/")

        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
