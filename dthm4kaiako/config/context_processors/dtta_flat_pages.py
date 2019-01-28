"""Context processor for displaying flat pages for DTTA navbar."""

from dtta.models import Page


def dtta_flat_pages(request):
    """Return a dictionary containing system version number.

    Returns:
        Dictionary containing version number to add to context.
    """
    pages = Page.objects.filter(published=True).order_by('order_number')
    return {"DTTA_FLAT_PAGES": pages}
