from tests.BaseTestWithDB import BaseTestWithDB


class DeletingApplicationsViaApplicationsViewTest(BaseTestWithDB):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.language = "en"
