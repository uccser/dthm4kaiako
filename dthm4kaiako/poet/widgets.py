"""Widgets for POET forms."""

from django.forms.widgets import NumberInput, RadioSelect, TextInput


class ResourcePreviewWithPK(NumberInput):
    """Widget for resource."""

    template_name = 'poet/widgets/resource.html'

    def __init__(self, resource, number):
        """Initialise widget.

        Args:
            resource (Resource): Resource for widget.
            number (int): Number resource in form.
        """
        super().__init__()
        self.resource = resource
        self.number = number

    def get_context(self, name, value, attrs):
        """Extra context for widget."""
        context = super().get_context(name, value, attrs)
        context['resource'] = self.resource
        context['number'] = self.number
        return context


class ProgressOutcomeTableRadioSelect(RadioSelect):
    """Widget for progress outcome table picker."""

    template_name = 'poet/widgets/po-table.html'
    option_template_name = 'poet/widgets/po-radio-select.html'

    def get_context(self, name, value, attrs):
        """Extra context for widget."""
        context = super().get_context(name, value, attrs)
        if hasattr(self, 'percentage_data'):
            context['percentage_data'] = self.percentage_data
            context['percentage_statement'] = self.percentage_statement
        return context


class TextArea(TextInput):
    """Widget for feedback text area."""

    template_name = 'poet/widgets/text-area.html'
