"""
Django settings for production environment.

- Load secret values from files.
"""

from .base import *  # noqa
from .base import env

# TODO: Review
# See https://docs.djangoproject.com/en/1.10/ref/settings/
ALLOWED_HOSTS = ["*"]

with open(env("DEPLOYMENT_ENVIRONMENT_FILE")) as file:  # noqa: F405
    DEPLOYMENT_ENVIRONMENT = file.read().strip()
PRODUCTION_ENVIRONMENT = DEPLOYMENT_ENVIRONMENT == "production"
STAGING_ENVIRONMENT = DEPLOYMENT_ENVIRONMENT == "staging"


# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Raises ImproperlyConfigured exception if DJANGO_SECRET_KEY not in os.environ
with open(env("DJANGO_SECRET_KEY_FILE")) as file:  # noqa: F405
    SECRET_KEY = file.read().strip()


# URL Configuration
# ------------------------------------------------------------------------------

if PRODUCTION_ENVIRONMENT:  # noqa: F405
    PREPEND_WWW = True
else:
    PREPEND_WWW = False

# Exempt Google App Engine cron job URLs from HTTPS to function correctly.
SECURE_REDIRECT_EXEMPT = [
    r'^/?cron/.*',
]

# DATABASE CONFIGURATION
# ----------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases

# Read in secret values
with open(env("POSTGRES_DB_FILE")) as file:  # noqa: F405
    POSTGRES_DB = file.read().strip()
with open(env("POSTGRES_USER_FILE")) as file:  # noqa: F405
    POSTGRES_USER = file.read().strip()
with open(env("POSTGRES_PASSWORD_FILE")) as file:  # noqa: F405
    POSTGRES_PASSWORD = file.read().strip()

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": POSTGRES_DB,
        "USER": POSTGRES_USER,
        "PASSWORD": POSTGRES_PASSWORD,
        "HOST": env("POSTGRES_HOST"),  # noqa: F405
        "PORT": env("POSTGRES_PORT"),  # noqa: F405
        "ATOMIC_REQUESTS": True,
    }
}


# SECURITY CONFIGURATION
# ------------------------------------------------------------------------------
# See https://docs.djangoproject.com/en/dev/ref/middleware/#module-django.middleware.security
# and https://docs.djangoproject.com/en/dev/howto/deployment/checklist/#run-manage-py-check-deploy

# set this to 60 seconds and then to 518400 when you can prove it works
# SECURE_HSTS_SECONDS = 60
# SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
# SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool("DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True)  # noqa: F405
# SECURE_CONTENT_TYPE_NOSNIFF = env.bool("DJANGO_SECURE_CONTENT_TYPE_NOSNIFF", default=True)  # noqa: F405
# SECURE_BROWSER_XSS_FILTER = True
# SESSION_COOKIE_SECURE = True
# SESSION_COOKIE_HTTPONLY = True
# SECURE_SSL_REDIRECT = env.bool("DJANGO_SECURE_SSL_REDIRECT", default=True)  # noqa: F405
# CSRF_COOKIE_SECURE = True
# CSRF_COOKIE_HTTPONLY = True
# X_FRAME_OPTIONS = "DENY"

# API KEYS
# ------------------------------------------------------------------------------
with open(env("GOOGLE_DRIVE_API_KEY_FILE")) as file:  # noqa: F405
    GOOGLE_DRIVE_API_KEY = file.read().strip()

# MAPS (django-map-widgets)
# ------------------------------------------------------------------------------
with open(env("GOOGLE_MAPS_API_KEY_FILE")) as file:  # noqa: F405
    GOOGLE_MAPS_API_KEY = file.read().strip()
MAP_WIDGETS["GOOGLE_MAP_API_KEY"] = GOOGLE_MAPS_API_KEY  # noqa: F405

# STORAGES
# ------------------------------------------------------------------------------
# https://django-storages.readthedocs.io/en/latest/backends/gcloud.html
INSTALLED_APPS += ['storages']  # noqa F405
DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
with open(env("GOOGLE_CLOUD_STORAGE_BUCKET_MEDIA_NAME_FILE")) as file:  # noqa: F405
    GS_BUCKET_NAME = file.read().strip()
GS_FILE_OVERWRITE = False
GS_DEFAULT_ACL = 'publicRead'

# TEMPLATES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES[0]['OPTIONS']['loaders'] = [  # noqa F405
    (
        'django.template.loaders.cached.Loader',
        [
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ]
    ),
]
# Disable APP_DIRS when custom loaders are specified.
TEMPLATES[0]['APP_DIRS'] = False  # noqa F405

# EMAIL
# ------------------------------------------------------------------------------
with open(env("MAILGUN_API_KEY_FILE")) as file:  # noqa: F405
    MAILGUN_API_KEY = file.read().strip()

ANYMAIL = {
    'MAILGUN_API_KEY': MAILGUN_API_KEY,
}
EMAIL_BACKEND = 'anymail.backends.mailgun.EmailBackend'
DEFAULT_FROM_EMAIL = env(
    'DJANGO_DEFAULT_FROM_EMAIL',
    default='dthm4kaiako <noreply@dthm4kaiako.ac.nz>'
)
# https://docs.djangoproject.com/en/dev/ref/settings/#server-email
SERVER_EMAIL = env('DJANGO_SERVER_EMAIL', default=DEFAULT_FROM_EMAIL)
# https://docs.djangoproject.com/en/dev/ref/settings/#email-subject-prefix
EMAIL_SUBJECT_PREFIX = env('DJANGO_EMAIL_SUBJECT_PREFIX', default='[dthm4kaiako] ')
# Email settings for all AllAuth
ACCOUNT_EMAIL_SUBJECT_PREFIX = EMAIL_SUBJECT_PREFIX


# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL regex.
# ADMIN_URL = env('DJANGO_ADMIN_URL')


# reCAPTCHA
# ------------------------------------------------------------------------------
with open(env("RECAPTCHA_PUBLIC_KEY_FILE")) as file:  # noqa: F405
    RECAPTCHA_PUBLIC_KEY = file.read().strip()

with open(env("RECAPTCHA_PRIVATE_KEY_FILE")) as file:  # noqa: F405
    RECAPTCHA_PRIVATE_KEY = file.read().strip()


# Sample Data
# ------------------------------------------------------------------------------
with open(env("SAMPLE_DATA_ADMIN_PASSWORD_FILE")) as file:  # noqa: F405
    SAMPLE_DATA_ADMIN_PASSWORD = file.read().strip()

with open(env("SAMPLE_DATA_USER_PASSWORD_FILE")) as file:  # noqa: F405
    SAMPLE_DATA_USER_PASSWORD = file.read().strip()
