"""Views for events application."""

from django.views import generic
from django.utils.timezone import now
from django_filters.views import FilterView
from utils.mixins import RedirectToCosmeticURLMixin
from events.models import (
    Event,
    Location,
    EventApplication,
)
from events.filters import UpcomingEventFilter, PastEventFilter
from events.utils import create_filter_helper, organise_schedule_data
from .forms import EventApplicationForm, TermsAndConditionsForm
from django.shortcuts import render
from users.forms import UserUpdateDetailsForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin


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


    def does_application_exist(self, user):
        """Determines if the user has submitted an application to attend the event.
        The user must also be logged in to see if they have.
        
        Returns:
            True if the user has an application and is logged in, otherwise False.
        """ 

        return EventApplication.objects.filter(event=self.object.pk, user=user).exists() and user.is_authenticated


    def get_context_data(self, **kwargs):
        """Provide the context data for the event view.

        Returns:
            Dictionary of context data.
        """
        context = super().get_context_data(**kwargs)
        context['sponsors'] = self.object.sponsors.all()
        context['organisers'] = self.object.organisers.all()
        context['schedule'] = organise_schedule_data(
            self.object.sessions.all().prefetch_related('locations')
        )
        context['locations'] = self.object.locations.all()

        user = self.request.user
        context['has_user_applied'] = self.does_application_exist(user)

        return context


class LocationDetailView(RedirectToCosmeticURLMixin, generic.DetailView):
    """View for a specific location."""

    model = Location
    context_object_name = 'location'


class EventApplicationsView(generic.ListView, LoginRequiredMixin):
    """View for listing all a user's event applications."""

    template_name = 'events/event_applications.html'
    model = EventApplication
    context_object_name = 'event_applications'


@login_required
def delete_application_via_application_page(request, pk):
    """ Allowing a user to delete an existing event application from their event applications page."""

    event_application = get_object_or_404(EventApplication, pk=pk)

    if request.method == 'POST':
        event_application.delete()
        return HttpResponseRedirect(reverse("events:event_applications"))

    return render(request, 'event_applications.html')


@login_required
def delete_application_via_event_page(request, pk):
    """ Allowing a user to delete an existing event application from the event details page."""

    event_application = get_object_or_404(EventApplication, pk=pk)

    if request.method == 'POST':
        event_application.delete()
        return HttpResponseRedirect(reverse("events:event", kwargs={'pk': event.pk, 'slug': event.slug}))

    return render(request, 'event_details.html')


@login_required
def apply_for_event(request, pk):
    """ View for event application/registration form and saving it as an EventApplication. 

        request: HTTP request 
        pk: event's primary key

        We create a new application if it doesn't already exist, otherwise we allow the user to update their existing application.
    """

    event = Event.objects.get(pk=pk)
    user = request.user

    event_application_form = None
    user_update_details_form = None
    terms_and_conditions_form = None

    if request.method == 'GET':
        # Prior to creating/updating registration form
        
        event_application_form = EventApplicationForm()
        user_update_details_form = UserUpdateDetailsForm()
        terms_and_conditions_form = TermsAndConditionsForm()


    elif request.method == 'POST':
        # If creating a new application or updating existing application (as Django forms don't support PUT)

        event_application_form = EventApplicationForm(request.POST)
        user_update_details_form = UserUpdateDetailsForm(request.POST)
        terms_and_conditions_form = TermsAndConditionsForm(request.POST)

        if event_application_form.is_valid() and user_update_details_form.is_valid() and terms_and_conditions_form.is_valid():
            user.first_name = user_update_details_form.cleaned_data['first_name']
            user.last_name = user_update_details_form.cleaned_data['last_name']
            all_dietary_reqs = user_update_details_form.cleaned_data['dietary_requirements']
            user.dietary_requirements.set(all_dietary_reqs)
            user.save()

            if user.event_applications.filter(event=event).exists():
                # Update existing event application
                event_application = user.event_applications.get(event=event)
                new_applicant_type = event_application_form.cleaned_data['applicant_type']
                event_application.applicant_type = new_applicant_type
                event_application.save()
                messages.success(request, "Updated event application successfully")
                return HttpResponseRedirect(reverse("events:event", kwargs={'pk': event.pk, 'slug': event.slug})) # Return to event detail page

            else:
                # Create new event application
                new_applicant_type = event_application_form.cleaned_data['applicant_type']
                event_application = EventApplication.objects.create(event=event,user=user,applicant_type=new_applicant_type)
                messages.success(request, 'New event application created successfully')
                return HttpResponseRedirect(reverse("events:event", kwargs={'pk': event.pk, 'slug': event.slug})) # Return to event detail page

    return render(request, 'events/apply.html', {'event': event, 'event_application_form': event_application_form, 'user_form': user_update_details_form, 'terms_and_conditions_form': terms_and_conditions_form })
