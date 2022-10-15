"""Unit tests for cancel event view"""

from django.urls import reverse
from http import HTTPStatus
from events.models import Event
from users.models import User
from tests.BaseTestWithDB import BaseTestWithDB
import datetime

class CancelEventURLTest(BaseTestWithDB):

    @classmethod
    def tearDownTestData(cls):
        Event.objects.all().delete()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def test_cancel_event_view_returns_200_when_event_exists_and_logged_in(self):
        '''Redirect to manage event page.'''
        event = Event.objects.create(
            name="Security in CS",
            description="description",
            registration_type=2,
            start=datetime.datetime(2023, 2, 13),
            end=datetime.datetime(2023, 2, 14),
            accessible_online=False,
            published=True
        )
        event.save()
        user = User.objects.create_user(
            username='kate',
            first_name='Kate',
            last_name='Bush',
            email='kate@uclive.ac.nz',
            password='potato',
        )
        user.save()
        event.event_staff.set([user])
        event.save()
        self.client.force_login(user)
        kwargs = {
            'pk': event.pk,
            }
        url = reverse('events:cancel_event', kwargs=kwargs)
        response = self.client.post(url)
        self.assertEqual(HTTPStatus.FOUND, response.status_code)
        self.assertEqual(response['Location'], f'/events/manage/{event.pk}/')

    def test_cancel_event_view_returns_302_when_event_exists_and_not_logged_in(self):
        '''Redirect to login page.'''
        event = Event.objects.create(
            name="Security in CS",
            description="description",
            registration_type=2,
            start=datetime.datetime(2023, 2, 13),
            end=datetime.datetime(2023, 2, 14),
            accessible_online=False,
            published=True
        )
        event.save()
        updated_event = Event.objects.filter(pk=1)
        updated_event.update(published=True)
        kwargs = {
            'pk': event.pk,
            }
        url = reverse('events:cancel_event', kwargs=kwargs)
        response = self.client.post(url)
        self.assertEqual(HTTPStatus.FOUND, response.status_code)
        self.assertEqual(response['Location'], f'/accounts/login/?next=/events/manage/cancel_event/{event.pk}/')

    def test_cancel_event_view_returns_200_when_event_exists_and_logged_in_and_not_staff(self):
        '''Redirect to all staff events page.'''
        event = Event.objects.create(
            name="Security in CS",
            description="description",
            registration_type=2,
            start=datetime.datetime(2023, 2, 13),
            end=datetime.datetime(2023, 2, 14),
            accessible_online=False,
            published=True
        )
        event.save()
        user = User.objects.create_user(
            username='kate',
            first_name='Kate',
            last_name='Bush',
            email='kate@uclive.ac.nz',
            password='potato',
        )
        user.save()
        event.event_staff.set([user])
        event.save()
        self.client.force_login(user)
        kwargs = {
            'pk': event.pk,
            }
        url = reverse('events:cancel_event', kwargs=kwargs)
        response = self.client.post(url)
        self.assertEqual(HTTPStatus.FOUND, response.status_code)
        self.assertEqual(response['Location'], f'/events/manage/')
