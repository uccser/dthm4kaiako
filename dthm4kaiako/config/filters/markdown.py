from django import template
from django.utils.safestring import mark_safe
from django.template.defaultfilters import stringfilter
from markdownx.utils import markdownify

register = template.Library()


@register.filter
@stringfilter
def markdown(raw_markdown):
    return mark_safe(markdownify(raw_markdown))
