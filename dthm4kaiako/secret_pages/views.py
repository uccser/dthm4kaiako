"""Views for secret pages application."""

from django.shortcuts import render, get_object_or_404
from django.conf import settings
from secret_pages.models import SecretPage


def secret_page_view(request, slug):
    """View of a secret page.

    Args:
        request (Request): Request from user.
        slug (str): Slug captured in URL.

    Returns:
        HTTP response.
    """
    page = get_object_or_404(
        SecretPage,
        slug=slug,
        active=True,
    )
    template = settings.SECRET_PAGES_TEMPLATE_TEMPLATE.format(page.template)
    return render(request, template)
