"""Context processor for API keys needed for templates."""

from django.conf import settings


def api_keys(request):
    """Return a dictionary containing API keys for templates.

    Be aware any keys provided here can be publically read in
    a rendered page's source code.

    Args:
        request (Request): The HTTP request.

    Returns:
        Dictionary containing API keys for templates.
    """
    return {
        "GOOGLE_MAPS_API_KEY": settings.GOOGLE_MAPS_API_KEY,
    }
