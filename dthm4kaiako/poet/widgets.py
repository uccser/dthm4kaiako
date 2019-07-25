from django.forms.widgets import RadioSelect


class ProgressOutcomeTableRadioSelect(RadioSelect):

    template_name = 'poet/widgets/po-table.html'
    option_template_name = 'poet/widgets/po-radio-select.html'
