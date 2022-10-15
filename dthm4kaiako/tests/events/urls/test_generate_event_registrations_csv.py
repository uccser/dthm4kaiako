"""Unit tests for generate_event_registrations_csv url"""

from tests.BaseTestWithDB import BaseTestWithDB


class GenerateEventRegistrationsCSVURLTest(BaseTestWithDB):

    @classmethod
    def tearDownTestData(cls):
        pass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)