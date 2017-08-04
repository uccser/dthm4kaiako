"""Administration configuration for the events application."""

from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.db import models
from tinymce.widgets import TinyMCE


class PageAdmin(FlatPageAdmin):
    """Override all text fields to use TinyMCE widget."""

    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }


admin.site.unregister(FlatPage)
admin.site.register(FlatPage, PageAdmin)
