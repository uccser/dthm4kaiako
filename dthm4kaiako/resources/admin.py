"""Module for admin configuration for the resources application."""

from django.contrib import admin
from resources.models import (
    Resource,
)


admin.site.register(Resource)
