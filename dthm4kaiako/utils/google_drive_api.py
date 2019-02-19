"""Module of functions that interact with the Google Drive API."""

import re
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from django.conf import settings


def get_google_drive_mimetype(url):
    """For a given Google Drive URL, return the document MIME type.

    Args:
        url (str): URL to determine MIME type for.

    Returns:
        MIME type if found, None otherwise.
    """
    file_id = re.search(r'[-\w]{25,}', url).group()
    service = build('drive', 'v3', developerKey=settings.GOOGLE_DRIVE_API_KEY, cache_discovery=False)
    request = service.files().get(fileId=file_id)
    try:
        response = request.execute()
    except HttpError:
        response = dict()
    return response.get('mimeType', None)
