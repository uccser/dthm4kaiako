"""Module for admin configuration for the Get Started application."""

import logging
from django.contrib import admin
from get_started.models import (
    Component,
)

logger = logging.getLogger(__name__)


class ComponentAdmin(admin.ModelAdmin):
    """Admin view for a Get Started component."""

    model = Component
    list_display = ('order_number', 'name', 'visibility', )
    ordering = ('order_number', )
    save_on_top = True

admin.site.register(Component, ComponentAdmin)
