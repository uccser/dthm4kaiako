from .google_cloud_file import GoogleCloudFile
from django.conf import settings
from django.core.files.storage import Storage
from google.cloud.storage.client import Client
from google.cloud.exceptions import GoogleCloudError
from google.oauth2 import service_account
import environ
import logging
import json
import mimetypes

logger = logging.getLogger(__name__)


class GoogleCloudStorage(Storage):

    def __init__(self, option=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.env = environ.Env()
        self.bucket = self.retrieve_bucket()

    def retrieve_bucket(self):
        project = self.env("GOOGLE_PROJECT")
        service_account_file = json.loads(self.env("GOOGLE_APPLICATION_CREDENTIALS"))
        credentials = service_account.Credentials.from_service_account_info(service_account_file)
        client = Client(project=project, credentials=credentials)
        return client.bucket("cs4teachers-static")

    def _open(self, name, mode="rb"):
        return GoogleCloudFile(name, mode, self.bucket)

    def exists(self, name):
        blob = self.bucket.blob(name)
        return blob.exists()

    def _save(self, name, content):
        mimetype = mimetypes.guess_type(name)[0]
        try:
            blob = self.bucket.blob(name)
            blob.upload_from_file(content, content_type=mimetype)
            return blob.public_url

        except GoogleCloudError as e:
            message = "Upload of file {} failed with error: {}"
            message.format(name, e)
            logger.error(message)
            return None

    def url(self, name):
        # return "/media/{}".format(name)
        pass

    def delete(self, name):
        blob = self.bucket.blob(name)
        blob.delete()
