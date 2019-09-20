"""Views for general application."""

from django.shortcuts import render, get_object_or_404
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
    return render(request, page.template)
