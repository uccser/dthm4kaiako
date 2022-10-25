"""Utility functions for events application."""

from django.utils.timezone import localdate, localtime
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Layout,
    Row,
    Column,
    Field,
    Div,
    HTML,
    Submit,
)

FILTER_HELPER_RESET_HTML_TEMPLATE = '<a href="{{% url "{}" %}}" class="btn btn-danger">Reset</a>'


class Day():
    """Class for organising time slots in schedule."""

    def __init__(self, datetime):
        """Create day object for tracking time slots."""
        self.date = localdate(datetime)
        self.time_slots = []


class TimeSlot():
    """Class for organising sessions in schedule."""

    def __init__(self, start_datetime, end_datetime):
        """Create time slot object for tracking sessions."""
        self.start = localtime(start_datetime)
        self.end = localtime(end_datetime)
        self.sessions = []


def organise_schedule_data(sessions):
    """Organises sessions for displaying in schedule.

    Returns:
        List of Day objects, each containing a list of TimeSlot objects, each containing a list of sessions.

    Example:
        [
            Day[
                TimeSlot[
                    Session,
                ],
                TimeSlot[
                    Session,
                    Session,
                    Session,
                ],
                TimeSlot[
                    Session,
                    Session,
                ],
            ],
            Day[
                TimeSlot[
                    Session,
                    Session,
                ],
                TimeSlot[
                    Session,
                    Session,
                ],
            ],
        ]
    """
    schedule_data = []
    for session in sessions:
        # If day list is empty or doesn't match last day, add day object.
        session_day = Day(session.start)
        if not schedule_data or not session_day.date == schedule_data[-1].date:
            schedule_data.append(session_day)

        # If last day's timeslot list is empty or doesn't match last
        # timeslot, add timeslot object.
        session_time_slot = TimeSlot(session.start, session.end)
        previous_time_slot = None
        if schedule_data[-1].time_slots:
            previous_time_slot = schedule_data[-1].time_slots[-1]

        if (
            not previous_time_slot or
            not (
                session_time_slot.start == previous_time_slot.start and
                session_time_slot.end == previous_time_slot.end
            )
        ):
            session_time_slot.sessions.append(session)
            schedule_data[-1].time_slots.append(session_time_slot)
        else:
            previous_time_slot.sessions.append(session)
    return schedule_data


def create_filter_helper(reset_url_pattern):
    """Return filter formatting helper.

    Args:
        reset_url_pattern (str): URL to set reset button to.

    Returns:
        Crispy-forms form helper.
    """
    filter_formatter = FormHelper()
    filter_formatter.form_method = 'get'
    filter_formatter.layout = Layout(
        Row(
            Column(
                Field(
                    'locations__region',
                    css_class='form-control form-control-sm',
                ),
                css_class='col-sm-12 col-md-4 mb-0',
            ),
            Column(
                Field(
                    'accessible_online',
                    css_class='form-control form-control-sm',
                ),
                css_class='form-group col-sm-12 col-md-4 mb-0',
            ),
            Column(
                Field(
                    'organisers',
                    css_class='form-control form-control-sm',
                ),
                css_class='form-group col-sm-12 col-md-4 mb-0',
            ),
        ),
        Div(
            HTML(FILTER_HELPER_RESET_HTML_TEMPLATE.format(reset_url_pattern)),
            Submit('submit', 'Filter events', css_class='btn-success'),
            css_class='d-flex justify-content-between',
        )
    )
    return filter_formatter


def can_view_event_management_content(request, event):
    """Return True if the user is event staff for the event management page."""
    user = request.user
    return user in event.event_staff.all()


def convert_string_list_to_one_string(listToConvert):
    """Convert list to string.

    Returns:
        A string of values separated by &'s.
    """
    if len(listToConvert) == 1:
        return listToConvert[0]
    else:
        newBigString = ""
        for i in range(0, len(listToConvert)):
            currentString = listToConvert[i]
            if i == len(listToConvert) - 1:
                newBigString += currentString
            else:
                newBigString += currentString + " & "
        return newBigString
