import pytest
from django.test import TestCase
from events.models import Event, Location

pytestmark = pytest.mark.django_db

class UserModelTests(TestCase):

    def test_is_register_or_apply:
        #TODO: write tests for is_register_or_apply property