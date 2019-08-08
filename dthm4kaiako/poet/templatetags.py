"""Module for the custom POET template tags."""

from django import template
from django.template.loader import render_to_string

register = template.Library()

DYNAMIC_HEAT_ELEMENT_WIDTH = 150  # pixels


@register.simple_tag(takes_context=True)
def render_heat_element(context, **kwargs):
    """Render heatmap element.

    Args:
        context (dict): Dictionary of view context.

    Returns:
        Rendered HTML string.
    """
    STYLE_TEMPLATE = """
    background: linear-gradient(
        90deg,
        rgba(255, 0, 0, 0) 0%,
        rgba(255, 0, 0, {opacity:.2f}) 50%,
        rgba(255, 0, 0, 0) 100%
    );
    width: {width:.2f}px;
    """
    if 'progress_outcome' in context:
        percentage = context['progress_outcome'].percentage
    else:
        percentage = context['percentage_data'].get(context['choice']['value'], 0)
    opacity = 0.2 + (0.8 * percentage)
    width = int(DYNAMIC_HEAT_ELEMENT_WIDTH * percentage)
    element_context = {
        'style': STYLE_TEMPLATE.format(opacity=opacity, width=width),
        'percentage': percentage * 100,
    }
    return render_to_string('poet/widgets/heat-element.html', element_context)
