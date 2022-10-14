"""Unit tests for event registrations csv model"""

from events.models import (
    EventRegistrationsCSV,
)
from events.models import EventRegistrationsCSV
import pytz
from tests.BaseTestWithDB import BaseTestWithDB

NEW_ZEALAND_TIME_ZONE = pytz.timezone('Pacific/Auckland')


class EventRegistrationsCSVTests(BaseTestWithDB):

    pass
