"""Context processor for displaying menu items for DTTA navbar."""

from dtta.models import Page, Project


def dtta_menu(request):
    """Return a dictionary containing items for DTTA navbar.

    Returns:
        Dictionary containing items for DTTA navbar.
    """
    planning_pages = Page.objects.filter(page_type=Page.PAGE_PLANNING, published=True).order_by('order_number')
    document_pages = Page.objects.filter(page_type=Page.PAGE_DOCUMENT, published=True).order_by('order_number')
    projects = Project.objects.filter(published=True).order_by('order_number')
    return {
        "DTTA_PLANNING_PAGES": planning_pages,
        "DTTA_DOCUMENT_PAGES": document_pages,
        "DTTA_PROJECTS": projects,
    }
