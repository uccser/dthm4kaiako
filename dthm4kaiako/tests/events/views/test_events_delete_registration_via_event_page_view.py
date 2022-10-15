from tests.BaseTestWithDB import BaseTestWithDB
from django.urls import reverse
from http import HTTPStatus
from django.test.utils import override_settings
from users.models import User
from events.models import (
    Event,
)
import datetime
import pytz
NEW_ZEALAND_TIME_ZONE = pytz.timezone('Pacific/Auckland')

class DeletingApplicationsViaEventDetailViewTest(BaseTestWithDB):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.language = "en"
