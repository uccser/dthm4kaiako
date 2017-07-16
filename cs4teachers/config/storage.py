"""Module for custom Django storage for storing files on Google Cloud Platform."""

from .google_cloud_file import GoogleCloudFile
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
    """Custom Django storage for storing files on Google Cloud Platform."""

    def __init__(self, option=None, *args, **kwargs):
        """Create the GoogleCloudStorage object."""
        super().__init__(*args, **kwargs)
        self.env = environ.Env()
        self.bucket = self.retrieve_bucket()

    def retrieve_bucket(self):
        """Return bucket used for storing files.

        Returns:
            Bucket object.
        """
        project = self.env("GOOGLE_PROJECT")
        service_account_file = json.loads(self.env("GOOGLE_APPLICATION_CREDENTIALS"))
        credentials = service_account.Credentials.from_service_account_info(service_account_file)
        client = Client(project=project, credentials=credentials)
        return client.bucket("cs4teachers-static")

    def _open(self, name, mode="rb"):
        """Mechanism used by the Django storage class to open the file.

        Called by Storage.open().

        Args:
            name (str): Name of the file.
            mode (str): Mode to open the file.

        Returns:
            GoogleCloudFile object of the file.
        """
        return GoogleCloudFile(name, mode, self.bucket)

    def exists(self, name):
        """Return boolean if file already exists in storage.

        Args:
            name (str): Name of file.

        Returns:
            True if a file referenced by the given name already exists in the
            storage system, or False if the name is available for a new file.
        """
        blob = self.bucket.blob(name)
        return blob.exists()

    def _save(self, name, content):
        """Mechanism used by the Django storage class to save the file.

        Called by Storage.save().

        Args:
            name (str): Name of the file.
            content (File): Content of the file.

        Returns:
            Actual name of the file saved (may be different to name given) (str).
        """
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

    def delete(self, name):
        """Delete a file.

        Args:
            name (str): Name of file to delete.
        """
        blob = self.bucket.blob(name)
        blob.delete()

    def url(self, name):
        """Return URL where the file referenced by name can be accessed.

        Args:
            name (str): Name of file to delete.
        """
        return self.bucket.blob(name).public_url
