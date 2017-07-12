"""Logic for a file that would be in a google cloud bucket."""
from django.core.files.base import File
from django.utils.encoding import force_bytes
from google.cloud.storage.blob import Blob
from google.cloud.exceptions import NotFound
from tempfile import SpooledTemporaryFile
import io
import logging
import mimetypes

logger = logging.getLogger(__name__)


class GoogleCloudFile(File):
    """File logic for reading and writing to Google Cloud bucket files."""

    def __init__(self, name, mode, bucket):
        """Create a GoogleCloudFile handler.

        Args:
            name: The name of the file within the bucket (string).
            mode: A string of the file mode to open with (string).
            bucket: The bucket to load and save to (Bucket).
        """
        self.name = name
        self.mode = mode
        self.storage = storage

        self._mimetype = mimetypes.guess_type(name)[0]
        self._is_dirty = False
        self._file = None
        self._blob = bucket.get_blob(name)

        if not self.blob and "w" in mode:
            self.blob = Blob(self.name, storage.bucket)
        elif not self.blob and "r" in mode:
            message = "{} file was not found."
            message.format(name)
            raise NotFound(message=message)

        self.open(mode)

    @property
    def size(self):
        """Get the size of the file.

        Returns:
            The size of the file (int).
        """
        if self._is_dirty:
            if hasattr(self.file, 'size'):
                return self.file.size
            if hasattr(self.file, 'tell') and hasattr(self.file, 'seek'):
                pos = self.file.tell()
                self.file.seek(0, os.SEEK_END)
                size = self.file.tell()
                self.file.seek(pos)
                return size
            raise AttributeError("Unable to determine the file's size.")
        return self.blob.size

    def _get_file(self):
        """Get the underlying file object.

        Returns:
            The underlying file object (stream).
        """
        if self._file is None:
            self.open()
        return self._file

    def _set_file(self, value):
        """Set the underlying file object.

        Args:
            value: The new file object (stream).
        """
        self._file = value

    file = property(_get_file, _set_file)

    def open(mode=None):
        """Open or reopen the file.

        Args:
            mode: The mode to file as, similar to pythons open
                function (string).
        """
        if mode is not None:
            self.mode = mode
        self._file = None
        self._is_dirty = False

        self._file = SpooledTemporaryFile(mode="w+b", suffix=".GoogleCloudFile")
        self.blob.download_to_file(self._file)
        if "a" not in self.mode:
            self._file.seek(0)

    def read(self, num_bytes=None):
        """Read from file.

        Args:
            num_bytes: The number of bytes to read from the file (int).
        Returns:
            The bytes read (bytes).
        """
        if "r" not in self.mode:
            raise AttributeError("File was not opened in read mode.")

        if num_bytes is None:
            num_bytes = -1

        return super(GoogleCloudFile, self).read(num_bytes)

    def write(self, content):
        """Write to the file.

        Args:
            content: Something to write to the file, if not bytes
            will attempt to convert (object).
        """
        if "w" not in self.mode or "a" not in self.mode:
            raise AttributeError("File was not opened in write mode.")

        self._is_dirty = True
        return super(GoogleCloudFile, self).write(force_bytes(content))

    def close(self):
        """Close the file, and save out changes."""
        if self._file is not None:
            if ("w" in self.mode or "a" in self.mode) and self._is_dirty:
                self._file.seek(0)
                self.blob.upload_from_file(self._file, content_type=self.mime_type)
            self._file.close()
            self._file = None
