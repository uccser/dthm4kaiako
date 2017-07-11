from django.conf import settings
from django.core.files.storage import Storage
from google.cloud.storage.client import Client
from google.oauth2 import service_account
import environ
import json


class GoogleCloudStorage(Storage):

    def __init__(self, option=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.env = environ.Env()
        self.bucket = self.retrieve_bucket()

    def retrieve_bucket(self):
        project = self.env.read_env("GOOGLE_PROJECT")
        service_account_file = json.load(self.env.read_env("GOOGLE_APPLICATION_CREDENTIALS"))
        credentials = service_account.Credentials.from_service_account_info(service_account_file)
        client = Client(project=project, credentials=credentials)
        return client.bucket("cs4teachers-static")

    def _open(self, name, mode="rb"):
        return

    def exists(self, name):
        return False

    def _save(self, name, content):
        blob = self.bucket.blob(name)
        blob.upload_from_file(content)
        return blob.public_url

    def url(self, name):
        # return "/media/{}".format(name)
        pass

    def delete(self, name):
        blob = self.bucket.blob(name)
        blob.delete()
