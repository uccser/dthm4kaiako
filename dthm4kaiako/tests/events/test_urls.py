from django.urls import reverse, resolve

class EventURLTest():

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def test_upcoming__reverse_provides_correct_url():
        assert(reverse("events:upcoming") == "/events/upcoming")


    def test_upcoming__resolve_provides_correct_view_name():
        assert(resolve("/events/upcoming/").view_name == "events:upcoming")


    def test_past__reverse_provides_correct_url():
        assert(reverse("events:past") == "/events/past")


    def test_past__resolve_provides_correct_view_name():
        assert(resolve("/events/past/").view_name == "events:past")


    # def test_event_detail__reverse_provides_correct_url_with_slug():
    #     kwargs = {
    #         pk = 1,
    #         slug = "CS-conference",
    #     }
    #     url = reverse("events:event", kwargs=kwargs)
    #     self.assertEqual(url, "/events/1/CS-conference/")

    
    def test_event_detail__resolve_provides_correct_view_name_with_slug():
        pass


    # def test_location():
    #     kwargs = {
    #         pk = 1,
    #     }
    #     url = reverse("events:location", kwargs=kwargs)
    #     self.assertEqual(url, "/location/1/")


    def test_applications__reverse_provides_correct_url():
        assert(reverse("events:applications") == "/events/applications")


    def test_applications__resolve_provides_correct_view_name():
        assert(resolve("/events/applications/").view_name == "events:applications")


    # def test_register__reverse_provides_correct_url():
    #     kwargs = {
    #         pk = 1,
    #     }
    #     url = reverse("events:register", kwargs=kwargs)
    #     self.assertEqual(url, "/events/register/1/")


    def test_register__resolve_provides_correct_view_name():
        pass
    
    
