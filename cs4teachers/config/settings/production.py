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

# DATABASE CONFIGURATION
# ----------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    "default": env.db("DATABASE_URL"),  # noqa: F405
}
DATABASES["default"]["ATOMIC_REQUESTS"] = True
