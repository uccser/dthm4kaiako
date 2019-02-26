"""Views for the general application."""

from django.http import HttpResponse
from django.core.management import call_command


def health_check(request):
    """Return health check response for Google App Engine.

    Returns a 200 HTTP response for Google App Engine to detect the system
    is running.
    """
    return HttpResponse(status=200)


def cron_rebuild_index(request):
    """Rebuild search index when triggered by cron job.

    Returns:
        200 HTTP response when valid cron job call is made.
        403 HTTP resoponse when invalid source.
    """
    if request.META.get('X-Appengine-Cron'):
        call_command('rebuild_index', noinput='')
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=403)
