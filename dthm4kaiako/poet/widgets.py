"""Widgets for POET forms."""

from django.forms.widgets import NumberInput, RadioSelect


class ResourcePDFPreviewWithPK(NumberInput):
    """Widget for resource."""

    template_name = 'poet/widgets/resource.html'

    def __init__(self, resource, number):
        """Initialise widget.

        Args:
            Resource for
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
