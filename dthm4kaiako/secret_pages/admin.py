"""Module for admin configuration for the secret pages application."""

from django.contrib import admin
from secret_pages.models import SecretPage


class SecretPageAdmin(admin.ModelAdmin):
    """Configuration for displaying secret pages in admin."""

    list_display = ('name', 'active', 'slug', 'template')
    ordering = ('name', 'active', 'slug', 'template')


admin.site.register(SecretPage, SecretPageAdmin)
