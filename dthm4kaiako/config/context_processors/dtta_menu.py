"""Context processor for displaying menu items for DTTA navbar."""

from dtta.models import Page, Project


def dtta_menu(request):
    """Return a dictionary containing items for DTTA navbar.

    Returns:
        Dictionary containing items for DTTA navbar.
    """
    pages = Page.objects.filter(published=True).order_by('order_number')
    projects = Project.objects.filter(published=True).order_by('order_number')
    return {"DTTA_PAGES": pages, "DTTA_PROJECTS": projects}
