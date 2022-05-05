"""Settings for local environment, built upon base settings."""

from .base import *  # noqa
from .base import env
import logging

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env('DJANGO_SECRET_KEY', default='DJANGO_SECRET_KEY_FOR_LOCAL_DEVELOPMENT')
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['*']


# DATABASE CONFIGURATION
# ----------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': env('POSTGRES_DB'),  # noqa: F405
        'USER': env('POSTGRES_USER'),  # noqa: F405
        'PASSWORD': env('POSTGRES_PASSWORD'),  # noqa: F405
        'HOST': env('POSTGRES_HOST'),  # noqa: F405
        'PORT': env('POSTGRES_PORT'),  # noqa: F405
        'ATOMIC_REQUESTS': True,
    }
}


# CACHES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': ''
    }
}

# TEMPLATES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG  # noqa F405

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-host
EMAIL_HOST = 'mailhog'
# https://docs.djangoproject.com/en/dev/ref/settings/#email-port
EMAIL_PORT = 1025

# django-debug-toolbar
# ------------------------------------------------------------------------------
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#prerequisites
INSTALLED_APPS += ['debug_toolbar']  # noqa F405
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#middleware
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']  # noqa F405
# https://django-debug-toolbar.readthedocs.io/en/latest/configuration.html#debug-toolbar-config


def show_django_debug_toolbar(request):
    """Show Django Debug Toolbar in every request when running locally.

    Args:
        request: The request object.
    """
    return True


DEBUG_TOOLBAR_CONFIG = {
    'DISABLE_PANELS': [
        'debug_toolbar.panels.redirects.RedirectsPanel',
        'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    ],
    'SHOW_TEMPLATE_CONTEXT': True,
    'SHOW_TOOLBAR_CALLBACK': show_django_debug_toolbar,
}
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#internal-ips
INTERNAL_IPS = ['127.0.0.1', '10.0.2.2']

# django-extensions
# ------------------------------------------------------------------------------
# https://django-extensions.readthedocs.io/en/latest/installation_instructions.html#configuration
INSTALLED_APPS += ['django_extensions']  # noqa F405

# Google Drive
# ------------------------------------------------------------------------------
GOOGLE_DRIVE_API_KEY = env('GOOGLE_DRIVE_API_KEY', default='GOOGLE_DRIVE_API_KEY_FOR_LOCAL_DEVELOPMENT')

# MAPS (django-map-widgets)
# ------------------------------------------------------------------------------
GOOGLE_MAPS_API_KEY = env('GOOGLE_MAPS_API_KEY', default='')
MAP_WIDGETS["GOOGLE_MAP_API_KEY"] = GOOGLE_MAPS_API_KEY  # noqa F405

# reCAPTCHA
# ------------------------------------------------------------------------------
# Use test keys
RECAPTCHA_PUBLIC_KEY = '6LeG0TIcAAAAACAMZ92F_Yvd6TQ62YdOkpqZAVh4'
RECAPTCHA_PRIVATE_KEY = '6LeG0TIcAAAAAH52RGgEPsHHHfh_uzMur6Ml2j7t'

# SVG
# ------------------------------------------------------------------------------
# Load SVGs from build folder for quicker loading
SVG_DIRS.append(os.path.join(str(ROOT_DIR.path("build")), "svg"))  # noqa: F405

# LOGGING
# ------------------------------------------------------------------------------
# Based off https://lincolnloop.com/blog/django-logging-right-way/
# Suppress these loggers in local development for less noise in logs
logging.getLogger('gunicorn.access').handlers = []  # noqa F405
logging.getLogger('gunicorn.error').handlers = []  # noqa F405
