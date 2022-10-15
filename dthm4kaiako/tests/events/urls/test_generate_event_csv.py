"""Unit tests for generate_event_csv url"""

from django.urls import reverse, resolve
from tests.BaseTestWithDB import BaseTestWithDB


class GenerateEventCSVURLTest(BaseTestWithDB):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_valid_generate_event_csv_url(self):
        url = reverse('events:generate_event_csv')
        expected_url = "/events/manage/generate_event_csv/"
        self.assertEqual(url, expected_url)

    def test_generate_event_csv_resolve_provides_correct_view_name(self):
        self.assertEqual(resolve("/events/manage/generate_event_csv/").view_name, "events:generate_event_csv")
