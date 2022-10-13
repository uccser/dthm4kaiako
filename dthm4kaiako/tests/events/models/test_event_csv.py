"""Unit tests for event CSV model"""

from django.test import TestCase
from events.models import EventCSV
import pytz
from tests.BaseTestWithDB import BaseTestWithDB

NEW_ZEALAND_TIME_ZONE = pytz.timezone('Pacific/Auckland')


class EventCSVTests(TestCase):

    pass
