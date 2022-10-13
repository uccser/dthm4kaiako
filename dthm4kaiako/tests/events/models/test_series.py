"""Unit tests for series model"""

from events.models import Series
import pytz
from tests.BaseTestWithDB import BaseTestWithDB

NEW_ZEALAND_TIME_ZONE = pytz.timezone('Pacific/Auckland')


class SeriesTests(BaseTestWithDB):

    # ------------------------------- tests for __str__ ----------------------------
    
    def test_str_representation(self):
        series = Series.objects.create(
            id=1,
            name='Artificial Intelligence series',
            abbreviation='AI series',
            description='Some description',
        )
        series.save()
        self.assertEqual(
            str(series),
            series.name
        )
