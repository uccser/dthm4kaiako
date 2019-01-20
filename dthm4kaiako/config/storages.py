"""Custom storages for seperating static and media files on Google Cloud Platform.

See:
- http://stackoverflow.com/questions/10390244/
- https://stackoverflow.com/a/18046120/104731
"""

from storages.backends.gcloud import GoogleCloudStorage


class StaticRootGoogleCloudStorage(GoogleCloudStorage):
    """Data for storing static files with django-storages."""

    location = 'static'


class MediaRootGoogleCloudStorage(GoogleCloudStorage):
    """Data for storing media files with django-storages."""

    location = 'media'
    file_overwrite = False
