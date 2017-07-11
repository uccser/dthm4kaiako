from django.conf import settings
from django.core.files.storage import Storage
from google.cloud.storage.client import Client
from google.oauth2 import service_account
import environ


class GoogleCloudStorage(Storage):

    def __init__(self, option=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bucket = retrieve_bucket()
        self.env = environ.Env()

    def _open(self, name, mode="rb"):
        pass

    def _save(name, content):
        pass

    def retrieve_bucket(self):
        service_account_file = self.env.read_env("GOOGLE_APPLICATION_CREDENTIALS")
        credentials = service_account.Credentials.from_service_account_info(service_account_file)
        client = Client(project=project, credentials=credentials)
