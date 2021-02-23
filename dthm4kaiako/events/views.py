"""Views for events application."""

from django.views import generic
from django.utils.timezone import now
from django_filters.views import FilterView
from utils.mixins import RedirectToCosmeticURLMixin
from events.models import (
    Event,
    EventApplication,
    EventVoucher,
)
from events.filters import UpcomingEventFilter, PastEventFilter
from events.utils import create_filter_helper
from events.forms import EventRegistrationForm, TermsAndConditionsForm
from users.forms import UserUpdateForm
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render


class HomeView(generic.TemplateView):
    """View for event homepage."""

    template_name = 'events/home.html'

    def get_context_data(self, **kwargs):
        """Provide the context data for the event homepage view.

        Returns:
            Dictionary of context data.
        """
        context = super().get_context_data(**kwargs)
        future_events = Event.objects.filter(published=True).filter(end__gte=now()).order_by('start').prefetch_related(
            'organisers',
            'locations',
            'sponsors',
        ).select_related(
            'series',
        )
        raw_map_locations = {}
        for event in future_events:
            for location in event.locations.all():
                key = location.pk
                if location.pk not in raw_map_locations:
                    # Create basic location information
                    raw_map_locations[key] = {
                        'coords': {'lat': location.coords.y, 'lng': location.coords.x},
                        'title': location.name,
                        'text': '<div class="map-info-title">{}</div>'.format(location.name),
                    }
                raw_map_locations[key]['text'] += '<p class="mb-0"><a href="{}">{:%-d %b %Y} - {}</a></p>'.format(
                    event.get_absolute_url(),
                    event.start,
                    event.name
                )
        context['raw_map_locations'] = list(raw_map_locations.values())
        return context


class EventUpcomingView(FilterView):
    """View for listing upcoming events."""

    # TODO: Add pagination
    filterset_class = UpcomingEventFilter
    context_object_name = 'events'
    template_name = 'events/upcoming_events.html'

    def get_context_data(self, **kwargs):
        """Provide the context data for the upcoming events view.

        Returns:
            Dictionary of context data.
        """
        context = super().get_context_data(**kwargs)
        context['filter_formatter'] = create_filter_helper("events:upcoming")
        return context


class EventPastView(FilterView):
    """View for listing past events."""

    # TODO: Add pagination
    filterset_class = PastEventFilter
    context_object_name = 'events'
    template_name = 'events/past_events.html'

    def get_context_data(self, **kwargs):
        """Provide the context data for the past events view.

        Returns:
            Dictionary of context data.
        """
        context = super().get_context_data(**kwargs)
        context['filter_formatter'] = create_filter_helper("events:past")
        return context


class EventDetailView(RedirectToCosmeticURLMixin, generic.DetailView):
    """View for a specific event."""

    model = Event
    context_object_name = 'event'

    def get_queryset(self):
        """Only show published events.

        Returns:
            Events filtered by published boolean.
        """
        return Event.objects.filter(published=True).prefetch_related('locations')

    def get_context_data(self, **kwargs):
        """Provide the context data for the event view.

        Returns:
            Dictionary of context data.
        """
        context = super().get_context_data(**kwargs)
        context['sponsors'] = self.object.sponsors.all()
        context['organisers'] = self.object.organisers.all()
        context['sessions'] = self.object.sessions.all().prefetch_related('locations')
        context['locations'] = self.object.locations.all()
        return context



@login_required
def register(request, pk):
    """View for registering for an event

    Args:
        request (Request): The HTTP request.
        pk (int): The primary key for the Event the user is registering for.
    """

    user = request.user
    event = Event.objects.get(pk=pk)
    if request.method == 'POST':
        event_form = EventRegistrationForm(request.POST)
        # Have to overwrite queryset again
        event_form.fields['applicant_type'].queryset = event.applicant_types.all()
        user_form = UserUpdateForm(request.POST)
        terms_and_conditions_form = TermsAndConditionsForm(request.POST)
        if 'voucher' in request.POST and request.POST['voucher'] != '':
            try:
                voucher = EventVoucher.objects.get(
                    code=request.POST['voucher'],
                    user=request.user
                )
            except EventVoucher.DoesNotExist:
                event_form.add_error('voucher', 'Sorry, that is not a valid voucher code.')

        if user_form.is_valid() and event_form.is_valid() and terms_and_conditions_form.is_valid():
            # save user data
            user.first_name = user_form.cleaned_data['first_name']
            user.last_name = user_form.cleaned_data['last_name']
            user.workplace = user_form.cleaned_data['workplace']
            user.city = user_form.cleaned_data['city']
            user.cell_phone_number = user_form.cleaned_data['cell_phone_number']
            user.medical_notes = user_form.cleaned_data['medical_notes']
            user.billing_address = user_form.cleaned_data['billing_address']
            dietary_requirements = user_form.cleaned_data['dietary_requirements']
            user.dietary_requirements.set(dietary_requirements)
            # check if event application already exists
            # TODO: Handle event cost logic
            if user.event_applications.filter(event=event).exists():
                # update application
                application = user.event_applications.filter(event=event)
                applicant_type = event_form.cleaned_data['applicant_type']
                application.applicant_type = applicant_type
                application.save()
            else:
                applicant_type = event_form.cleaned_data['applicant_type']
                event_application = EventApplication.objects.create(
                    event=event,
                    user=user,
                    applicant_type=applicant_type
                )
            user.save()
            return HttpResponseRedirect(reverse("events:thanks"))

    else:
        user_form = UserUpdateForm()
        event_form = EventRegistrationForm()
        event_form.fields['applicant_type'].queryset = event.applicant_types.all()
        terms_and_conditions_form = TermsAndConditionsForm()

    return render(
        request,
        'events/event_registration_form.html',
        {
            'event_form': event_form,
            'user_form': user_form,
            'terms_and_conditions_form': terms_and_conditions_form,
            'event': event,
        }
    )


class EventApplicationView(LoginRequiredMixin, generic.ListView):

    model = EventApplication
    template_name = 'events/event_applications.html'

    def get_object(self):
        """Get object for template."""
        return self.request.user

    def get_context_data(self, **kwargs):
        """Provide the context data for the event applications view.

        Returns:
            Dictionary of context data.
        """
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['user_event_applications'] = EventApplication.objects.filter(user=self.request.user)
        return context
