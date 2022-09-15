from tests.BaseTestWithDB import BaseTestWithDB


class DeletingApplicationsViaEventDetailViewTest(BaseTestWithDB):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.language = "en"
