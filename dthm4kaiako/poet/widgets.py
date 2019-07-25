"""Widgets for POET forms."""

from django.forms.widgets import RadioSelect


class ProgressOutcomeTableRadioSelect(RadioSelect):
    """Widget for progress outcome table picker."""

    template_name = 'poet/widgets/po-table.html'
    option_template_name = 'poet/widgets/po-radio-select.html'
