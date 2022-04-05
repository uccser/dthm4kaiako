"""Core URL routing for Django system."""

from django.conf import settings
from django.urls import include, path
from django.http.response import HttpResponse
from django.views.generic import RedirectView
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.views import defaults as default_views
from config.views import get_release_and_commit
admin.site.login = login_required(admin.site.login)
admin.site.site_header = 'dthm4kaiako.ac.nz'
admin.site.site_title = admin.site.site_header

urlpatterns = [
    # Main applications
    path('', include('general.urls', namespace='general')),
    path('dtta/', include('dtta.urls', namespace='dtta')),
    path('events/', include('events.urls', namespace='events'),),
    path('users/', include('users.urls', namespace='users'),),
    path('resources/', include('resources.urls', namespace='resources')),
    path('ara-ako/', include('ara_ako.urls', namespace='ara_ako')),
    path('poet/', include('poet.urls', namespace='poet')),
    path('learning-area-cards/', include('learning_area_cards.urls', namespace='learning_area_cards')),
    path('s/', include('secret_pages.urls', namespace='secret_pages')),
    # Accounts application
    path('accounts/', include('allauth.urls')),
    # Admin application
    path(settings.ADMIN_URL, admin.site.urls),
    # Utility applications
    path('healthcheck/', HttpResponse),
    path('status/', view=get_release_and_commit, name="get-release-and-commit"),
    path('markdownx/', include('markdownx.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    # path('api/', include('rest_framework.urls')),
    # Redirects
    path('authentic-context-cards/', RedirectView.as_view(pattern_name='learning_area_cards:home', permanent=True)),
] + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            '400/',
            default_views.bad_request,
            kwargs={'exception': Exception('Bad Request!')},
        ),
        path(
            '403/',
            default_views.permission_denied,
            kwargs={'exception': Exception('Permission Denied')},
        ),
        path(
            '404/',
            default_views.page_not_found,
            kwargs={'exception': Exception('Page not Found')},
        ),
        path('500/', default_views.server_error),
    ]
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path('__debug__/', include(debug_toolbar.urls))] + urlpatterns
