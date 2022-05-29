"""Unit tests for users"""

import pytest
from django.test import TestCase
from events.models import (
    DietaryRequirement,
    User,
    Entity,
    )

pytestmark = pytest.mark.django_db

pytestmark = pytest.mark.django_db

class DietaryRequirementTests(TestCase):

    # ----------------------- tests for __str__ -----------------------

    def test_str_representation(self):
        pass 


class UserTests(TestCase):

    # ----------------------- tests for get_absolute_url -----------------------

    def test_get_absolute_url(self):
        pass 

    # ----------------------- tests for __str__ -----------------------

    def test_str_representation(self):
        pass 


class EntityTests(TestCase):

    # ----------------------- tests for __str__ -----------------------

    def test_str_representation(self):
        pass

    