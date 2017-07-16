from django.db import utils
from tests.BaseTest import BaseTest
from events.models import Sponsor


class SponsorModelTest(BaseTest):

    def test_sponsor(self):
        sponsor = self.event_data.create_sponsor(1)
        query_result = Sponsor.objects.get(name="Sponsor 1")
        self.assertEqual(
            query_result,
            sponsor
        )

    def test_sponsor_slug_must_be_unique(self):
        self.event_data.create_sponsor(1)
        self.assertRaises(
            utils.IntegrityError,
            self.event_data.create_sponsor,
            1
        )

    def test_sponsor_name(self):
        self.event_data.create_sponsor(1)
        query_result = Sponsor.objects.get(name="Sponsor 1")
        self.assertEqual(
            query_result.name,
            "Sponsor 1"
        )

    def test_sponsor_url(self):
        self.event_data.create_sponsor(1)
        query_result = Sponsor.objects.get(name="Sponsor 1")
        self.assertEqual(
            query_result.url,
            "https://www.1.com/"
        )

    def test_sponsor_str(self):
        sponsor = self.event_data.create_sponsor(1)
        self.assertEqual(sponsor.__str__(), "Sponsor 1")
