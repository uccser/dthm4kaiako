from django.test import TestCase
from django.urls import reverse, resolve


class EventURLTest(TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def test_upcoming__reverse_provides_correct_url(self):
        self.assertEqual(reverse("events:upcoming"), "/events/upcoming/")


    def test_upcoming__resolve_provides_correct_view_name(self):
        self.assertEqual(resolve("/events/upcoming/").view_name, "events:upcoming")


    def test_past__reverse_provides_correct_url(self):
        self.assertEqual(reverse("events:past"), "/events/past/")


    def test_past__resolve_provides_correct_view_name(self):
        self.assertEqual(resolve("/events/past/").view_name, "events:past")

    # TODO: fix - Failing
    def test_event_detail__reverse_provides_correct_url_with_slug(self):
        pk = 1,
        slug = "CS-conference"
        kwargs = kwargs={'pk' : pk, 'slug' : slug}
        url = reverse('events:event', kwargs=kwargs)
        self.assertEqual(url, '/events/event/1/CS-conference/')


    # TODO: fix - Failing
    def test_location(self):
        pk = 1,
        kwargs = {'pk' : pk}
        url = reverse("events:location", kwargs=kwargs)
        self.assertEqual(url, "/events/location/1/")


    def test_applications__reverse_provides_correct_url(self):
        self.assertEqual(reverse("events:event_applications"), "/events/applications/")


    def test_applications__resolve_provides_correct_view_name(self):
        self.assertEqual(resolve("/events/applications/").view_name, "events:event_applications")


    def test_register__reverse_provides_correct_url(self):
        kwargs = {'pk' : 1}
        url = reverse("events:apply", kwargs=kwargs)
        self.assertEqual(url, "/events/register/1/")


    def test_register__resolve_provides_correct_view_name(self):
        pass
    
    
