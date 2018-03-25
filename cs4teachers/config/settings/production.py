# -*- coding: utf-8 -*-
"""
Django settings for production environment.

- Load secret values from environment variables.
"""

from .base import *  # noqa: F403

# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Raises ImproperlyConfigured exception if DJANGO_SECRET_KEY not in os.environ
SECRET_KEY = env("DJANGO_SECRET_KEY")  # noqa: F405

# SECURITY WARNING: App Engine"s security features ensure that it is safe to
# have ALLOWED_HOSTS = ["*"] when the app is deployed. If you deploy a Django
# app not on App Engine, make sure to set an appropriate host here.
# See https://docs.djangoproject.com/en/dev/ref/settings/
ALLOWED_HOSTS = ["*"]

if env("DEPLOYMENT", default=None) == "prod":  # noqa: F405
    PREPEND_WWW = True
else:
    PREPEND_WWW = False

# DATABASE CONFIGURATION
# ----------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "cs4teachers",
        "USER": env("GOOGLE_CLOUD_SQL_DATABASE_USERNAME"),  # noqa: F405
        "PASSWORD": env("GOOGLE_CLOUD_SQL_DATABASE_PASSWORD"),  # noqa: F405
        "HOST": "/cloudsql/" + env("GOOGLE_CLOUD_SQL_CONNECTION_NAME"),  # noqa: F405
    }
}
DATABASES["default"]["ATOMIC_REQUESTS"] = True

# Allow all host headers
ALLOWED_HOSTS = ["*"]

# This ensures that Django will be able to detect a secure connection
# properly on Heroku.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# SECURITY CONFIGURATION
# ------------------------------------------------------------------------------
# See https://docs.djangoproject.com/en/dev/ref/middleware/#module-django.middleware.security
# and https://docs.djangoproject.com/en/dev/howto/deployment/checklist/#run-manage-py-check-deploy

# set this to 60 seconds and then to 518400 when you can prove it works
SECURE_HSTS_SECONDS = 60
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool("DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True)  # noqa: F405
SECURE_CONTENT_TYPE_NOSNIFF = env.bool("DJANGO_SECURE_CONTENT_TYPE_NOSNIFF", default=True)  # noqa: F405
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SECURE_SSL_REDIRECT = env.bool("DJANGO_SECURE_SSL_REDIRECT", default=True)  # noqa: F405
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = "DENY"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
        }
    }
}


# Static and media files
# ------------------------
INSTALLED_APPS += [  # noqa: F405
    "storages",
]
DEFAULT_FILE_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
GS_BUCKET_NAME = env("GOOGLE_CLOUD_STORAGE_BUCKET_NAME")  # noqa: F405
GS_FILE_OVERWRITE = False
STATIC_URL = "https://storage.googleapis.com/" + env("GOOGLE_CLOUD_STORAGE_BUCKET_NAME") + "/static/"  # noqa: F405

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#default-from-email
DEFAULT_FROM_EMAIL = env(  # noqa: F405
    "DJANGO_DEFAULT_FROM_EMAIL",
    default="cs4teachers.org.nz <noreply@cs4teachers.org.nz>"
)
# https://docs.djangoproject.com/en/dev/ref/settings/#server-email
SERVER_EMAIL = env("DJANGO_SERVER_EMAIL", default=DEFAULT_FROM_EMAIL)  # noqa: F405
# https://docs.djangoproject.com/en/dev/ref/settings/#email-subject-prefix
EMAIL_SUBJECT_PREFIX = env("DJANGO_EMAIL_SUBJECT_PREFIX", default="[cs4teachers.org.nz] ")  # noqa: F405

# Anymail (Mailgun)
# ------------------------------------------------------------------------------
# https://anymail.readthedocs.io/en/stable/installation/#installing-anymail
INSTALLED_APPS += ["anymail"]  # noqa F405
EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"
# https://anymail.readthedocs.io/en/stable/installation/#anymail-settings-reference
ANYMAIL = {
    "MAILGUN_API_KEY": env("MAILGUN_API_KEY"),  # noqa: F405
    "MAILGUN_SENDER_DOMAIN": env("MAILGUN_DOMAIN")  # noqa: F405
}
