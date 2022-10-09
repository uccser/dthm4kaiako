"""Views for events registration."""

# from turtle import heading
# from multiprocessing import context
from django.views import generic
from django.utils.timezone import now
from django_filters.views import FilterView
from utils.mixins import RedirectToCosmeticURLMixin
from events.models import (
    DeletedEventRegistration,
    Event,
    Location,
    EventRegistration,
    Address,
    RegistrationForm,
    Series,
    ParticipantType
)
from users.models import (
    DietaryRequirement,
    Entity,
    User
)
from events.filters import UpcomingEventFilter, PastEventFilter
from events.utils import create_filter_helper, organise_schedule_data
from .forms import (
    EventRegistrationForm,
    TermsAndConditionsForm,
    BillingDetailsForm,
    WithdrawEventRegistrationForm,
    ManageEventRegistrationForm,
    ManageEventDetailsForm,
    ManageEventRegistrationFormDetailsForm,
    BuilderFormForEventsCSV,
    BuilderFormForEventRegistrationsCSV,
    ParticipantTypeForm,
    ParticipantTypeCreationForm,
    ContactParticipantsForm,
    ManageEventDetailsReadOnlyForm,
    ManageEventRegistrationFormDetailsReadOnlyForm,
    ManageEventRegistrationReadOnlyForm,
)
from django.shortcuts import render, redirect
from users.forms import UserUpdateDetailsForm
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
import csv
from django.utils.html import format_html_join
from datetime import datetime
from django.core.mail import send_mail
from events.utils import can_view_event_management_content
import re

NON_EVENT_STAFF_ACCESS_MESSAGE = "Sorry, {1}, you are not a staff member of \"{2}\"."

PRIVACY_STATEMENT = (
    "PRIVACY STATEMENT: We care about your privacy. Only the necessary information " +
    "is collected for event organisers to run this event."
)


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

    def does_registration_exist(self, user):
        """Determine if the user has submitted an registration to attend the event.

        The user must also be logged in to see if they have.

        Returns:
            True if the user has an registration and is logged in, otherwise False.
        """
        return EventRegistration.objects.filter(event=self.object.pk, user=user).exists() and user.is_authenticated

    def get_registration_pk(self, user):
        """Return the primary key of the user's event registration of the event."""
        event_registration_pk = 0
        if EventRegistration.objects.filter(event=self.object.pk, user=user).exists():
            event_registration = EventRegistration.objects.get(event=self.object.pk, user=user)
            event_registration_pk = event_registration.pk
        return event_registration_pk

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
        context['is_event_staff'] = can_view_event_management_content(self.request, self.object)

        user = self.request.user

        if user.is_authenticated:
            if self.does_registration_exist(user):
                withdraw_event_registration_form = WithdrawEventRegistrationForm(self.request.POST)
                context['withdraw_event_registration_form'] = withdraw_event_registration_form
                context['has_user_applied'] = True
                context['registration_pk'] = self.get_registration_pk(user)
                context['event_registration'] = EventRegistration.objects.get(event=self.object.pk, user=user)
        else:
            context['user_is_authenticated'] = False

        return context


class LocationDetailView(RedirectToCosmeticURLMixin, generic.DetailView):
    """View for a specific location."""

    model = Location
    context_object_name = 'location'


class EventRegistrationsView(LoginRequiredMixin, generic.ListView):
    """View for listing all a user's event registrations."""

    template_name = 'events/event_registrations.html'
    model = EventRegistration

    def get_context_data(self, **kwargs):
        """Provide the context data for the event applictions view.

        Returns:
            Dictionary of context data.
        """
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.is_authenticated:
            today = datetime.today()
            event_registrations_upcoming = EventRegistration.objects.filter(
                user=user,
                event__start__gte=today
                ).order_by('event__start')
            event_registrations_past = EventRegistration.objects.filter(user=user, event__start__lte=today).order_by(
                '-event__start')
            context['event_registrations_upcoming'] = event_registrations_upcoming
            context['event_registrations_past'] = event_registrations_past
            context['user'] = self.request.user
            if len(event_registrations_upcoming) != 0:
                context['withdraw_event_registration_form'] = WithdrawEventRegistrationForm(self.request.POST)
        return context

    def get_object(self):
        """Retrieve the user object for the associated template."""
        return self.request.user


@login_required
def delete_registration_via_registration_page(request, pk):
    """Allow a user to delete an existing event registration from their event registrations page."""
    event_registration = EventRegistration.objects.get(pk=pk)
    event = Event.objects.get(pk=event_registration.event.pk)
    user = event_registration.user

    if event is None:
        return HttpResponseRedirect(reverse("events:home"))

    if event_registration is None or request.user != event_registration.user:
        return HttpResponseRedirect(reverse("events:event_registrations"))

    if request.method == 'POST':
        create_deleted_event_registration(event, request)
        event_registration.delete()
        user.save()
        messages.success(request, f'Your event registration for \"{event.name}\" has been withdrawn')
        return HttpResponseRedirect(reverse("events:event_registrations"))

    return render(request, 'events/event_registrations.html')


@login_required
def delete_registration_via_event_page(request, pk):
    """Allow a user to delete an existing event registration from their event registrations page."""
    event_registration = get_object_or_404(EventRegistration, pk=pk)
    event = Event.objects.get(pk=event_registration.event.pk)
    user = event_registration.user

    if event is None:
        return HttpResponseRedirect(reverse("events:home"))

    if event_registration is None or request.user != event_registration.user:
        return HttpResponseRedirect(reverse("events:home"))

    if request.method == 'POST':
        create_deleted_event_registration(event, request)
        event_registration.delete()
        user.save()
        messages.success(request, f'Your event registration for \"{event.name}\" has been withdrawn')
        return HttpResponseRedirect(reverse("events:event", kwargs={'pk': event.pk, 'slug': event.slug}))

    return render(request, 'event_details.html')


def create_deleted_event_registration(event, request):
    """Create DeletedEventRegistration based on the retrieved deletion reason and/or other reason for deletion."""
    reason = request.POST['withdraw_reason']
    other_reason = request.POST['other_reason_for_withdrawing']
    if other_reason != "":
        deleted_event_registration = DeletedEventRegistration.objects.create(
            withdraw_reason=reason,
            event=event,
            other_reason_for_withdrawing=other_reason
        )
    else:
        deleted_event_registration = DeletedEventRegistration.objects.create(
            withdraw_reason=reason,
            event=event,
        )
    deleted_event_registration.save()


def validate_event_registration_form(
            event_registration_form,
            user_update_details_form,
            terms_and_conditions_form,
            billing_required,
            billing_details_form,
            participant_type_form,
            request,
            is_physical_event
        ):
    """Validate that the event registration is valid.

    Also accommodates for the billing section and dietary requirements sections
    to be only validated if they are needed i.e. are rended.
    """
    if (
        event_registration_form.is_valid() and
        user_update_details_form.is_valid() and
        terms_and_conditions_form.is_valid() and
        (not billing_required or billing_details_form.is_valid()) and
        participant_type_form.is_valid()
    ):

        phone_number_pattern = re.compile(r"^[-\(\)\+\s\./0-9]*$")

        if is_physical_event and not emergency_details_valid(event_registration_form):
            messages.error(
                request,
                (
                    'Please provide emergency contact details.'
                )
            )
        elif is_physical_event and not phone_number_pattern.match(
            event_registration_form.cleaned_data['emergency_contact_phone_number']
        ):
            messages.error(
                request,
                (
                    'Invalid phone number. Phone number can include the area code, follow by any '
                    'number of numbers, - and spaces. E.g. (+64) 123 45 678, 123-45-678, 12345678'
                )
            )
        else:
            return True
    else:
        return False


def emergency_details_valid(event_registration_form):
    """Return True is emergency contact details are valid, else False."""
    if event_registration_form.is_valid():
        if (
            event_registration_form.cleaned_data['emergency_contact_first_name'] is None
            or event_registration_form.cleaned_data['emergency_contact_last_name'] is None
            or event_registration_form.cleaned_data['emergency_contact_phone_number'] is None
            or event_registration_form.cleaned_data['emergency_contact_relationship'] is None
        ):
            return False
        else:
            return True


def does_registration_exist(user, event):
    """Return True if event registration already exists for the given user and event."""
    return user.event_registrations.filter(event=event).exists()


@login_required
def register_for_event(request, pk):
    """View for event registration/registration form and saving it as an EventRegistration.

    request: HTTP request
    pk: event's primary key

    We create a new registration if it doesn't already exist, otherwise
    we allow the user to update their existing registration.
    """
    event = Event.objects.get(pk=pk)
    user = request.user

    event_registration_form = None
    user_update_details_form = None
    billing_details_form = None
    terms_and_conditions_form = None
    billing_required = not event.is_free
    display_catering_info = event.is_catered
    new_billing_email = None
    current_registration = None
    billing_physical_address = None
    billing_email_address = ""
    bill_to = ""
    participant_type_form = None
    new_participant_type = ""
    is_physical_event = not event.accessible_online

    registration_exists = does_registration_exist(user, event)

    if request.method == 'GET':
        # Prior to creating/updating registration form

        if registration_exists:
            current_registration = user.event_registrations.get(event=event)
            participant_type_form = ParticipantTypeForm(
                event,
                initial={'participant_type': current_registration.participant_type.pk}
            )
            event_registration_form = EventRegistrationForm(
                instance=current_registration,
                initial={'show_emergency_contact_fields': not event.accessible_online}
            )
            billing_physical_address = current_registration.billing_physical_address
            billing_email_address = current_registration.billing_email_address
            bill_to = current_registration.bill_to
        else:
            event_registration_form = EventRegistrationForm(
                initial={'show_emergency_contact_fields': not event.accessible_online}
            )
            participant_type_form = ParticipantTypeForm(event)

        user_update_details_form = UserUpdateDetailsForm(
            instance=user,
            initial={
                'show_dietary_requirements': event.is_catered,
                'show_medical_notes': not event.accessible_online,
                'email_address': user.email_address,
                'email_address_confirm': user.email_address,
                'mobile_phone_number': user.mobile_phone_number,
                'mobile_phone_number_confirm': user.mobile_phone_number,
                'how_we_can_best_look_after_you': user.medical_notes
            })  # autoload existing event registration's user data

        if billing_required:
            initial_billing_data = {'billing_email_address': billing_email_address, 'bill_to': bill_to}
            billing_details_form = BillingDetailsForm(
                instance=billing_physical_address,
                initial=initial_billing_data  # TODO: figure out how to autoload billing info
            )
        terms_and_conditions_form = TermsAndConditionsForm(
                # User must re-agree each time they update the form
                initial={
                    'I_agree_to_the_terms_and_conditions': False,
                }
            )

        if event.is_less_than_one_week_prior_event and event.is_catered:
            messages.warning(
                request,
                (
                    'Your dietary requirements may not be considered for catering due to '
                    'it being too close to the event commencing. '
                    f'Please consider contacting us at {event.contact_email_address}'
                )
            )

    elif request.method == 'POST':
        # If creating a new registration or updating existing registration (as Django forms don't support PUT)

        user_update_details_form = UserUpdateDetailsForm(
            request.POST,
            instance=user,
            initial={
                'show_dietary_requirements': event.is_catered,
                'show_medical_notes': not event.accessible_online,
                'email_address': user.email_address,
                'email_address_confirm': user.email_address,
                'mobile_phone_number': user.mobile_phone_number,
                'mobile_phone_number_confirm': user.mobile_phone_number,
                'how_we_can_best_look_after_you': user.medical_notes
            }
        )

        if does_registration_exist(user, event):
            current_registration = user.event_registrations.get(event=event)
            event_registration_form = EventRegistrationForm(request.POST, instance=current_registration)
        else:
            event_registration_form = EventRegistrationForm(request.POST)

        participant_type_form = ParticipantTypeForm(event, request.POST)

        if billing_required:
            initial_billing_data = {'billing_email_address': billing_email_address, 'bill_to': bill_to}
            billing_details_form = BillingDetailsForm(request.POST, initial=initial_billing_data)
        terms_and_conditions_form = TermsAndConditionsForm(request.POST)

        if validate_event_registration_form(
            event_registration_form,
            user_update_details_form,
            terms_and_conditions_form,
            billing_required,
            billing_details_form,
            participant_type_form,
            request,
            is_physical_event
           ):

            user.first_name = user_update_details_form.cleaned_data['first_name']
            user.last_name = user_update_details_form.cleaned_data['last_name']
            all_educational_entities = user_update_details_form.cleaned_data['educational_entities']
            user.educational_entities.set(all_educational_entities)
            user.user_region = user_update_details_form.cleaned_data['user_region']
            user.email_address = user_update_details_form.cleaned_data['email_address']
            user.mobile_phone_number = user_update_details_form.cleaned_data['mobile_phone_number']

            if event.accessible_online is False:
                user.medical_notes = user_update_details_form.cleaned_data['how_we_can_best_look_after_you']

            if display_catering_info:
                all_dietary_reqs = user_update_details_form.cleaned_data['dietary_requirements']
                user.dietary_requirements.set(all_dietary_reqs)
            user.save()

            new_participant_type_id = participant_type_form.cleaned_data['participant_type']
            new_participant_type = ParticipantType.objects.get(pk=int(new_participant_type_id))
            new_representing = event_registration_form.cleaned_data['representing']
            new_emergency_contact_first_name = event_registration_form.cleaned_data['emergency_contact_first_name']
            new_emergency_contact_last_name = event_registration_form.cleaned_data['emergency_contact_last_name']
            new_emergency_contact_relationship = event_registration_form.cleaned_data['emergency_contact_relationship']
            new_emergency_contact_phone_number = event_registration_form.cleaned_data['emergency_contact_phone_number']

            if billing_required:
                new_bill_to = billing_details_form.cleaned_data['bill_to']
                new_street_number = billing_details_form.cleaned_data['street_number']
                new_street_name = billing_details_form.cleaned_data['street_name']
                new_suburb = billing_details_form.cleaned_data['suburb']
                new_city = billing_details_form.cleaned_data['city']
                new_region = billing_details_form.cleaned_data['region']
                new_post_code = billing_details_form.cleaned_data['post_code']
                new_country = billing_details_form.cleaned_data['country']
                new_billing_email = billing_details_form.cleaned_data['billing_email_address']

                new_billing_address = Address.objects.create(
                    street_number=new_street_number,
                    street_name=new_street_name,
                    suburb=new_suburb,
                    city=new_city,
                    region=new_region,
                    post_code=new_post_code,
                    country=new_country,
                )
                new_billing_address.save()

                event_registration, created = EventRegistration.objects.update_or_create(
                    user=user, event=event,
                    defaults={
                        'participant_type': new_participant_type,
                        'representing': new_representing,
                        'billing_physical_address': new_billing_address,
                        'billing_email_address': new_billing_email,
                        'bill_to': new_bill_to,
                        'emergency_contact_first_name': new_emergency_contact_first_name,
                        'emergency_contact_last_name': new_emergency_contact_last_name,
                        'emergency_contact_relationship': new_emergency_contact_relationship,
                        'emergency_contact_phone_number': new_emergency_contact_phone_number,
                    }
                )
                event_registration.save()

            else:
                event_registration, created = EventRegistration.objects.update_or_create(
                    user=user,
                    event=event,
                    defaults={
                        'participant_type': new_participant_type,
                        'representing': new_representing,
                        'emergency_contact_first_name': new_emergency_contact_first_name,
                        'emergency_contact_last_name': new_emergency_contact_last_name,
                        'emergency_contact_relationship': new_emergency_contact_relationship,
                        'emergency_contact_phone_number': new_emergency_contact_phone_number,
                    }
                )
                event_registration.save()

            if registration_exists:
                # Update existing event registration
                messages.success(request, f"Your event registration for \"{event.name}\" has been updated")
                # Return to event detail page
                return HttpResponseRedirect(reverse("events:event", kwargs={'pk': event.pk, 'slug': event.slug}))

            else:
                # Create new event registration

                if event.registration_type == 1:
                    messages.success(
                        request,
                        f"Thank you for for registering for \"{event.name}\", {user.first_name}. " +
                        "We look forward to seeing you then!"
                    )
                elif event.registration_type == 2:
                    messages.success(
                        request,
                        f"Thank you for appling for \"{event.name}\", {user.first_name}. " +
                        "You registration will reviewed shortly by our event staff!"
                    )
                # Return to event detail page
                return HttpResponseRedirect(reverse("events:event", kwargs={'pk': event.pk, 'slug': event.slug}))

    context = {
        'event': event,
        'event_registration_form': event_registration_form,
        'user_form': user_update_details_form,
        'billing_details_form': billing_details_form,
        'billing_required': billing_required,
        'terms_and_conditions_form': terms_and_conditions_form,
        'withdraw_event_registration_form': WithdrawEventRegistrationForm(request.POST),
        'participant_type_form': participant_type_form,
        'registration_exists': registration_exists,
        'privacy_statement': PRIVACY_STATEMENT
    }

    return render(request, 'events/apply.html', context)


# TODO: add filter
class EventsManagementView(LoginRequiredMixin, generic.ListView):
    """View for a events management."""

    template_name = 'events/events_management.html'

    def get_context_data(self, **kwargs):
        """Provide the context data for the events management view.

        Returns:
            Dictionary of context data.
        """
        context = super().get_context_data(**kwargs)
        user = self.request.user

        self.request

        if user.is_authenticated:
            if Event.objects.filter(event_staff__pk=user.pk).exists():
                # TODO: order these
                today = datetime.today()
                context['events_user_is_staff_for_future'] = Event.objects.filter(
                    event_staff__pk=user.pk,
                    start__gte=today
                ).order_by('start')
                context['events_user_is_staff_for_past'] = Event.objects.filter(
                    event_staff__pk=user.pk,
                    start__lte=today
                ).order_by('-start')
                event_csv_builder_form = BuilderFormForEventsCSV()
                context['event_csv_builder_form'] = event_csv_builder_form
        return context

    def get_queryset(self):
        """Show all events.

        Returns:
            Events.
        """
        return Event.objects.all().order_by('name')


def is_in_past_or_cancelled(event):
    """Return True if event is in the past or it has been cancelled."""
    return event.end < now() or event.is_cancelled


@login_required
def manage_event(request, pk):
    """View for event management.

    Contains forms for each event related object (similar to that in Admin app).
    These can be viewed, updated (based on non-read only fields) and deleted.
    """
    event = Event.objects.get(pk=pk)

    if not can_view_event_management_content(request, event):
        messages.warning(
            request,
            NON_EVENT_STAFF_ACCESS_MESSAGE.format(request.user.first_name, event.name)
        )
        return HttpResponseRedirect(reverse("events:events_management"))

    event_registrations = EventRegistration.objects.filter(event=event)
    pending_event_registrations = EventRegistration.objects.filter(event=event, status=1)
    approved_event_registrations = EventRegistration.objects.filter(event=event, status=2)
    declined_event_registrations = EventRegistration.objects.filter(event=event, status=3)

    registration_form = event.registration_form
    context = {
        'event': event,
        'event_pk': event.pk
    }
    user = request.user

    if request.method == 'GET':

        context['event_registrations'] = event_registrations
        context['pending_event_registrations'] = pending_event_registrations
        context['approved_event_registrations'] = approved_event_registrations
        context['declined_event_registrations'] = declined_event_registrations
        context['registrations_csv_builder_form'] = BuilderFormForEventRegistrationsCSV()
        context['event_registrations'] = event_registrations
        context['registration_form_pk'] = registration_form.pk
        context['is_free'] = event.is_free
        context['participant_types'] = ParticipantType.objects.filter(events=event).order_by('-price', 'name')
        context['new_participant_form'] = ParticipantTypeCreationForm()
        context['update_participant_form'] = ParticipantTypeCreationForm()
        context['contact_participants_form'] = ContactParticipantsForm(
            initial={
                'from_email': event.contact_email_address,
                'name': user
                }
            )

        if is_in_past_or_cancelled(event):
            context['manage_event_details_form'] = ManageEventDetailsReadOnlyForm(instance=event)
            context['manage_registration_form_details_form'] = ManageEventRegistrationFormDetailsReadOnlyForm(
                instance=registration_form
            )
        else:
            context['manage_event_details_form'] = ManageEventDetailsForm(instance=event)
            context['manage_registration_form_details_form'] = ManageEventRegistrationFormDetailsForm(
                instance=registration_form
            )

        return render(request, 'events/event_management.html', context)


def user_dietary_requirements(registration):
    """Return a list of the participant's user's dietary requirements.

    This is based on the event registration submitted by the participant.
    """
    return format_html_join(
        '\n',
        '<li>{}</li>',
        registration.user.dietary_requirements.values_list('name'),
    )


@login_required
def manage_event_registration(request, pk_event, pk_registration):
    """View for managing event registrations."""
    event_registration = EventRegistration.objects.get(pk=pk_registration)
    event = event_registration.event

    if not can_view_event_management_content(request, event):
        messages.warning(
            request,
            NON_EVENT_STAFF_ACCESS_MESSAGE.format(request.user.first_name, event.name)
        )
        return HttpResponseRedirect(reverse("events:events_management"))

    context = {
        'event': event,
        'pk_event': pk_event,
        'pk_registration': pk_registration,
        'event_registration': event_registration
    }
    context['update_participant_form'] = ParticipantTypeForm(event, request.POST)

    user = User.objects.get(id=event_registration.user.pk)

    dietary_requirements = DietaryRequirement.objects.filter(users=user)
    educational_entities = Entity.objects.filter(users=user)

    if request.method == 'GET':
        if is_in_past_or_cancelled(event):
            manage_registration_form = ManageEventRegistrationReadOnlyForm(instance=event_registration)
        else:
            manage_registration_form = ManageEventRegistrationForm(
                event,
                initial={'participant_type': event_registration.participant_type.pk},
                instance=event_registration
            )

    elif request.method == 'POST':

        if is_in_past_or_cancelled(event):
            manage_registration_form = ManageEventRegistrationReadOnlyForm(request.POST, instance=event_registration)
        else:
            manage_registration_form = ManageEventRegistrationForm(
                event,
                request.POST,
                instance=event_registration,
                initial={'participant_type': event_registration.participant_type.pk},
            )

        if manage_registration_form.is_valid():

            updated_status = manage_registration_form.cleaned_data['status']
            updated_staff_comments = manage_registration_form.cleaned_data['staff_comments']
            updated_admin_billing_comments = manage_registration_form.cleaned_data['admin_billing_comments']
            update_paid = manage_registration_form.cleaned_data['paid']
            updated_participant_type_pk = manage_registration_form.cleaned_data['participant_type']

            updated_participant_type = ParticipantType.objects.get(pk=updated_participant_type_pk)
            registration = EventRegistration.objects.filter(pk=pk_registration)
            registration.update(
                status=updated_status,
                staff_comments=updated_staff_comments,
                admin_billing_comments=updated_admin_billing_comments,
                paid=update_paid,
                participant_type=updated_participant_type,
            )
            updated_event_registration = EventRegistration.objects.get(pk=pk_registration)
            updated_event_registration.save()

            messages.success(
                request,
                f"You have updated {event_registration.user.first_name} {event_registration.user.last_name}\'s " +
                "event registration"
            )
            return HttpResponseRedirect(reverse(
                "events:manage_event_registration",
                kwargs={'pk_event': pk_event, 'pk_registration': pk_registration}
                ))
        else:
            messages.warning(
                request,
                "Please resolve the invalid fields to update " +
                f"{event_registration.user.first_name} {event_registration.user.last_name}\'s event registration."
            )

    context['manage_registration_form'] = manage_registration_form
    context['dietary_requirements'] = dietary_requirements
    context['educational_entities'] = educational_entities
    context['is_event_staff'] = can_view_event_management_content(request, event)

    return render(request, 'events/manage_event_registration.html', context)


# TODO: add event staff access only
@login_required
def manage_event_details(request, pk):
    """Allow event staff to update event details as well as deleting the event if desired."""
    event = Event.objects.get(pk=pk)

    if not can_view_event_management_content(request, event):
        messages.warning(
            request,
            NON_EVENT_STAFF_ACCESS_MESSAGE.format(request.user.first_name, event.name)
        )
        return HttpResponseRedirect(reverse("events:events_management"))

    context = {
        'event': event,
    }
    # context['update_participant_form'] = ParticipantTypeCreationForm()

    if request.method == 'POST':
        manage_event_details_form = ManageEventDetailsForm(request.POST, instance=event)
        if manage_event_details_form.is_valid():

            updated_name = manage_event_details_form.cleaned_data['name']
            updated_description = manage_event_details_form.cleaned_data['description']
            updated_show_schedule = manage_event_details_form.cleaned_data['show_schedule']
            updated_featured = manage_event_details_form.cleaned_data['featured']
            updated_registration_type = manage_event_details_form.cleaned_data['registration_type']
            updated_registration_link = manage_event_details_form.cleaned_data['external_event_registration_link']
            updated_start = manage_event_details_form.cleaned_data['start']
            updated_end = manage_event_details_form.cleaned_data['end']
            updated_accessible_online = manage_event_details_form.cleaned_data['accessible_online']
            update_is_catered = manage_event_details_form.cleaned_data['is_catered']
            update_contact_email_address = manage_event_details_form.cleaned_data['contact_email_address']
            update_series = manage_event_details_form.cleaned_data['series']
            update_capacity = manage_event_details_form.cleaned_data['capacity']

            all_locations = manage_event_details_form.cleaned_data['locations']
            all_location_ids = [location.id for location in all_locations]
            event.locations.set(all_location_ids)

            all_sponsors = manage_event_details_form.cleaned_data['sponsors']
            all_sponsors_ids = [sponsor.id for sponsor in all_sponsors]
            event.sponsors.set(all_sponsors_ids)

            all_organisers = manage_event_details_form.cleaned_data['organisers']
            all_organisers_ids = [organiser.id for organiser in all_organisers]
            event.organisers.set(all_organisers_ids)

            all_event_staff = manage_event_details_form.cleaned_data['event_staff']
            all_event_staff_ids = [event_staff.id for event_staff in all_event_staff]
            event.event_staff.set(all_event_staff_ids)

            # TODO: update otherside of M2M relationships for locations, sponsors,
            # organisers, serieses and event staff

            Event.objects.filter(id=event.pk).update(
                name=updated_name,
                description=updated_description,
                show_schedule=updated_show_schedule,
                featured=updated_featured,
                registration_type=updated_registration_type,
                external_event_registration_link=updated_registration_link,
                start=updated_start,
                end=updated_end,
                accessible_online=updated_accessible_online,
                is_catered=update_is_catered,
                contact_email_address=update_contact_email_address,
                series=update_series,
                capacity=update_capacity,
            )
            event.save()
            messages.success(request, f'You have updated the event details of {event.name}')
            return HttpResponseRedirect(reverse("events:event_management", kwargs={'pk': event.pk}))
        else:
            messages.warning(
                request,
                f'Please resolve the invalid fields to update the details of \"{event.name}\".'
            )
    elif request.method == 'DELETE':
        event_name = event.name
        event.delete()
        messages.success(request, f'You have removed \"{event_name}\"')
        return HttpResponseRedirect(reverse("events:event_management", kwargs={'pk': event.pk}))

    context['manage_event_details_form'] = manage_event_details_form
    context['event'] = event
    context['event_pk'] = event.pk

    return render(request, 'events/event_management.html', context)


# TODO: add event staff access only
@login_required
def manage_event_registration_form_details(request, pk):
    """Allow event staff to update event registration form details.

    Note that registration_form is the RegistrationForm object (as per the model) and
    registration_form_details_form is a Form object (for UI).
    """
    registration_form = RegistrationForm.objects.get(pk=pk)
    event = registration_form.event

    if not can_view_event_management_content(request, event):
        messages.warning(
            request,
            NON_EVENT_STAFF_ACCESS_MESSAGE.format(request.user.first_name, event.name)
        )
        return HttpResponseRedirect(reverse("events:events_management"))

    context = {
        'registration_form': registration_form,
    }
    # context['update_participant_form'] = ParticipantTypeCreationForm()

    if request.method == 'POST':
        manage_registration_form_details_form = ManageEventRegistrationFormDetailsForm(
            request.POST,
            instance=registration_form
            )
        if manage_registration_form_details_form.is_valid():

            updated_open_datetime = manage_registration_form_details_form.cleaned_data['open_datetime']
            updated_close_datetime = manage_registration_form_details_form.cleaned_data['close_datetime']
            updated_terms_and_conditions = manage_registration_form_details_form.cleaned_data['terms_and_conditions']

            RegistrationForm.objects.filter(event_id=registration_form.pk).update(
                open_datetime=updated_open_datetime,
                close_datetime=updated_close_datetime,
                terms_and_conditions=updated_terms_and_conditions,
            )
            registration_form.save()
            messages.success(request, f'You have updated the event registration form details of {event.name}')
            return HttpResponseRedirect(reverse("events:event_management", kwargs={'pk': event.pk}))
        else:
            messages.warning(
                request,
                f'Please resolve the invalid fields to update the registration form details of \"{event.name}\".'
            )

    context['manage_registration_form_details_form'] = manage_registration_form_details_form
    context['event'] = event
    context['registration_form_pk'] = registration_form.pk
    context['event_pk'] = event.pk

    return render(request, 'events/event_management.html', context)


def convertStringListToOneString(listToConvert):
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


# TODO: fix UI bug where the validation error message only disappears
# if go back out and back to events management hub page
# TODO: add staff and admin permissions
@login_required
def generate_event_csv(request):
    """Generate a custom CSV of events' data."""
    event = Event.objects.get(pk=request.event.pk)

    if not can_view_event_management_content(request, event):
        messages.warning(
            request,
            NON_EVENT_STAFF_ACCESS_MESSAGE.format(request.user.first_name, event.name)
        )
        return HttpResponseRedirect(reverse("events:events_management"))

    if request.method == 'POST':
        builderFormForEventsCSV = BuilderFormForEventsCSV(request.POST)
        if builderFormForEventsCSV.is_valid():

            file_name = builderFormForEventsCSV.cleaned_data['file_name']

            first_wrote_titles = []

            if builderFormForEventsCSV.cleaned_data['event_name']:
                first_wrote_titles.append('event_name')
            if builderFormForEventsCSV.cleaned_data['description']:
                first_wrote_titles.append('description')
            if builderFormForEventsCSV.cleaned_data['published_status']:
                first_wrote_titles.append('published_status')
            if builderFormForEventsCSV.cleaned_data['show_schedule']:
                first_wrote_titles.append('show_schedule')
            if builderFormForEventsCSV.cleaned_data['featured_status']:
                first_wrote_titles.append('featured_status')
            if builderFormForEventsCSV.cleaned_data['registration_type']:
                first_wrote_titles.append('registration_type')
            if builderFormForEventsCSV.cleaned_data['external_event_registration_link']:
                first_wrote_titles.append('external_event_registration_link')
            if builderFormForEventsCSV.cleaned_data['start_datetime']:
                first_wrote_titles.append('start_datetime')
            if builderFormForEventsCSV.cleaned_data['end_datetime']:
                first_wrote_titles.append('end_datetime')
            if builderFormForEventsCSV.cleaned_data['accessible_online']:
                first_wrote_titles.append('accessible_online')
            if builderFormForEventsCSV.cleaned_data['is_free']:
                first_wrote_titles.append('is_free')
            if builderFormForEventsCSV.cleaned_data['locations']:
                first_wrote_titles.append('locations')
            if builderFormForEventsCSV.cleaned_data['sponsors']:
                first_wrote_titles.append('sponsors')
            if builderFormForEventsCSV.cleaned_data['organisers']:
                first_wrote_titles.append('organisers')
            if builderFormForEventsCSV.cleaned_data['series']:
                first_wrote_titles.append('series')
            if builderFormForEventsCSV.cleaned_data['is_catered']:
                first_wrote_titles.append('is_catered')
            if builderFormForEventsCSV.cleaned_data['contact_email_address']:
                first_wrote_titles.append('contact_email_address')
            if builderFormForEventsCSV.cleaned_data['event_staff']:
                first_wrote_titles.append('event_staff')
            if builderFormForEventsCSV.cleaned_data['is_cancelled']:
                first_wrote_titles.append('is_cancelled')
            if builderFormForEventsCSV.cleaned_data['approved_registrations_count']:
                first_wrote_titles.append('approved_registrations_count')
            if builderFormForEventsCSV.cleaned_data['pending_registrations_count']:
                first_wrote_titles.append('pending_registrations_count')
            if builderFormForEventsCSV.cleaned_data['declined_registrations_count']:
                first_wrote_titles.append('declined_registrations_count')
            if builderFormForEventsCSV.cleaned_data['withdrawn_registrations_count']:
                first_wrote_titles.append('withdrawn_registrations_count')

            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename= "{}.csv"'.format(file_name)

            # Create a csv writer
            writer = csv.writer(response)

            # Designate the model
            events = Event.objects.all()

            # Add column headings to the csv file
            writer.writerow(first_wrote_titles)

            for event in events:
                row = []

                if builderFormForEventsCSV.cleaned_data['event_name']:
                    row.append(event.name)
                if builderFormForEventsCSV.cleaned_data['description']:
                    row.append(event.description)
                if builderFormForEventsCSV.cleaned_data['published_status']:
                    row.append(event.published)
                if builderFormForEventsCSV.cleaned_data['show_schedule']:
                    row.append(event.show_schedule)
                if builderFormForEventsCSV.cleaned_data['featured_status']:
                    row.append(event.featured)
                if builderFormForEventsCSV.cleaned_data['registration_type']:
                    row.append(event.get_event_type_short)
                if builderFormForEventsCSV.cleaned_data['external_event_registration_link']:
                    row.append(event.external_event_registration_link)
                if builderFormForEventsCSV.cleaned_data['start_datetime']:
                    row.append(event.start)
                if builderFormForEventsCSV.cleaned_data['end_datetime']:
                    row.append(event.end)
                if builderFormForEventsCSV.cleaned_data['accessible_online']:
                    row.append(event.accessible_online)
                if builderFormForEventsCSV.cleaned_data['is_free']:
                    row.append(event.is_free)
                if builderFormForEventsCSV.cleaned_data['locations']:
                    locations = [location.name for location in Location.objects.filter(events=event)]
                    locations_string = convertStringListToOneString(locations)
                    row.append(locations_string)
                if builderFormForEventsCSV.cleaned_data['sponsors']:
                    sponsors = [sponsor.name for sponsor in Entity.objects.filter(sponsored_events=event)]
                    sponsors_string = convertStringListToOneString(sponsors)
                    row.append(sponsors_string)
                if builderFormForEventsCSV.cleaned_data['organisers']:
                    organisers = [organiser.name for organiser in Location.objects.filter(events=event)]
                    organisers_string = convertStringListToOneString(organisers)
                    row.append(organisers_string)
                if builderFormForEventsCSV.cleaned_data['series']:
                    series = [series.name for series in Series.objects.filter(events=event)]
                    series_string = convertStringListToOneString(series)
                    row.append(series_string)
                if builderFormForEventsCSV.cleaned_data['is_catered']:
                    row.append(event.is_catered)
                if builderFormForEventsCSV.cleaned_data['contact_email_address']:
                    row.append(event.contact_email_address)
                if builderFormForEventsCSV.cleaned_data['event_staff']:
                    staff = [str(user.first_name + user.last_name) for user in User.objects.filter(events=event)]
                    staff_string = convertStringListToOneString(staff)
                    row.append(staff_string)
                if builderFormForEventsCSV.cleaned_data['is_cancelled']:
                    row.append(event.is_cancelled)
                if builderFormForEventsCSV.cleaned_data['approved_registrations_count']:
                    row.append(event.registration_status_counts['approved'])
                if builderFormForEventsCSV.cleaned_data['pending_registrations_count']:
                    row.append(event.registration_status_counts['pending'])
                if builderFormForEventsCSV.cleaned_data['declined_registrations_count']:
                    row.append(event.registration_status_counts['declined'])
                if builderFormForEventsCSV.cleaned_data['withdrawn_registrations_count']:
                    row.append(event.registration_status_counts['withdrawn'])

                writer.writerow(row)

            return response

        else:
            messages.warning(request, 'Event registrations CSV builder form has an invalid field.')

    context = {
        'event_csv_builder_form': builderFormForEventsCSV,
        'events_user_is_staff_for': Event.objects.filter(event_staff__pk=request.user.pk)
    }

    return render(request, 'events/events_management.html', context)


# TODO: fix UI bug where the validation error message only disappears if go back out and back to event management page
# TODO: add staff and admin permissions
@login_required
def generate_event_registrations_csv(request, pk):
    """Generate a custom CSV of event registrations' data."""
    event = Event.objects.get(pk=pk)

    if not can_view_event_management_content(request, event):
        messages.warning(
            request,
            NON_EVENT_STAFF_ACCESS_MESSAGE.format(request.user.first_name, event.name)
        )
        return HttpResponseRedirect(reverse("events:events_management"))

    if request.method == 'POST':
        builderFormForEventRegistrationsCSV = BuilderFormForEventRegistrationsCSV(request.POST)
        if builderFormForEventRegistrationsCSV.is_valid():

            file_name = builderFormForEventRegistrationsCSV.cleaned_data['file_name']

            first_wrote_titles = []

            if builderFormForEventRegistrationsCSV.cleaned_data['event_name']:
                first_wrote_titles.append('event_name')
            if builderFormForEventRegistrationsCSV.cleaned_data['submitted_datetime']:
                first_wrote_titles.append('submitted_datetime')
            if builderFormForEventRegistrationsCSV.cleaned_data['updated_datetime']:
                first_wrote_titles.append('updated_datetime')
            if builderFormForEventRegistrationsCSV.cleaned_data['status']:
                first_wrote_titles.append('status')
            if builderFormForEventRegistrationsCSV.cleaned_data['participant_type']:
                first_wrote_titles.append('participant_type')
            if builderFormForEventRegistrationsCSV.cleaned_data['staff_comments']:
                first_wrote_titles.append('staff_comments')
            if builderFormForEventRegistrationsCSV.cleaned_data['participant_first_name']:
                first_wrote_titles.append('participant_first_name')
            if builderFormForEventRegistrationsCSV.cleaned_data['participant_last_name']:
                first_wrote_titles.append('participant_last_name')
            if builderFormForEventRegistrationsCSV.cleaned_data['dietary_requirements']:
                first_wrote_titles.append('dietary_requirements')
            if builderFormForEventRegistrationsCSV.cleaned_data['educational_entities']:
                first_wrote_titles.append('educational_entities')
            if builderFormForEventRegistrationsCSV.cleaned_data['region']:
                first_wrote_titles.append('region')
            if builderFormForEventRegistrationsCSV.cleaned_data['mobile_phone_number']:
                first_wrote_titles.append('mobile_phone_number')
            if builderFormForEventRegistrationsCSV.cleaned_data['email_address']:
                first_wrote_titles.append('email_address')
            if builderFormForEventRegistrationsCSV.cleaned_data['how_we_can_best_accommodate_them']:
                first_wrote_titles.append('how_we_can_best_accommodate_them')
            if builderFormForEventRegistrationsCSV.cleaned_data['representing']:
                first_wrote_titles.append('representing')
            if builderFormForEventRegistrationsCSV.cleaned_data['emergency_contact_first_name']:
                first_wrote_titles.append('emergency_contact_first_name')
            if builderFormForEventRegistrationsCSV.cleaned_data['emergency_contact_last_name']:
                first_wrote_titles.append('emergency_contact_last_name')
            if builderFormForEventRegistrationsCSV.cleaned_data['emergency_contact_relationship']:
                first_wrote_titles.append('emergency_contact_relationship')
            if builderFormForEventRegistrationsCSV.cleaned_data['emergency_contact_phone_number']:
                first_wrote_titles.append('emergency_contact_phone_number')
            if builderFormForEventRegistrationsCSV.cleaned_data['paid']:
                first_wrote_titles.append('paid')
            if builderFormForEventRegistrationsCSV.cleaned_data['bill_to']:
                first_wrote_titles.append('bill_to')
            if builderFormForEventRegistrationsCSV.cleaned_data['billing_physical_address']:
                first_wrote_titles.append('billing_physical_address')
            if builderFormForEventRegistrationsCSV.cleaned_data['billing_email_address']:
                first_wrote_titles.append('billing_email_address')
            if builderFormForEventRegistrationsCSV.cleaned_data['admin_billing_comments']:
                first_wrote_titles.append('admin_billing_comments')

            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename= "{}.csv"'.format(file_name)

            # Create a csv writer
            writer = csv.writer(response)

            # Designate the model
            event_registrations = EventRegistration.objects.filter(event=event)

            # Add column headings to the csv file
            writer.writerow(first_wrote_titles)

            for event_registration in event_registrations:
                user = event_registration.user
                row = []

                if builderFormForEventRegistrationsCSV.cleaned_data['event_name']:
                    row.append(event_registration.event.name)
                if builderFormForEventRegistrationsCSV.cleaned_data['submitted_datetime']:
                    row.append(event_registration.submitted)
                if builderFormForEventRegistrationsCSV.cleaned_data['updated_datetime']:
                    row.append(event_registration.updated)
                if builderFormForEventRegistrationsCSV.cleaned_data['status']:
                    row.append(event_registration.status_string_for_user)
                if builderFormForEventRegistrationsCSV.cleaned_data['participant_type']:
                    row.append(event_registration.participant_type)
                if builderFormForEventRegistrationsCSV.cleaned_data['staff_comments']:
                    row.append(event_registration.staff_comments)
                if builderFormForEventRegistrationsCSV.cleaned_data['participant_first_name']:
                    row.append(user.first_name)
                if builderFormForEventRegistrationsCSV.cleaned_data['participant_last_name']:
                    row.append(user.last_name)
                if builderFormForEventRegistrationsCSV.cleaned_data['dietary_requirements']:
                    row.append(convertStringListToOneString([dR.name for dR in user.dietary_requirements.all()]))
                if builderFormForEventRegistrationsCSV.cleaned_data['educational_entities']:
                    row.append(convertStringListToOneString(
                        [entity.name for entity in user.educational_entities.all()]
                        )
                    )
                if builderFormForEventRegistrationsCSV.cleaned_data['region']:
                    row.append(user.get_user_region_display())
                if builderFormForEventRegistrationsCSV.cleaned_data['mobile_phone_number']:
                    row.append(user.mobile_phone_number)
                if builderFormForEventRegistrationsCSV.cleaned_data['email_address']:
                    row.append(user.email_address)
                if builderFormForEventRegistrationsCSV.cleaned_data['how_we_can_best_accommodate_them']:
                    row.append(user.medical_notes)
                if builderFormForEventRegistrationsCSV.cleaned_data['representing']:
                    row.append(event_registration.representing)
                if builderFormForEventRegistrationsCSV.cleaned_data['emergency_contact_first_name']:
                    row.append(event_registration.emergency_contact_first_name)
                if builderFormForEventRegistrationsCSV.cleaned_data['emergency_contact_last_name']:
                    row.append(event_registration.emergency_contact_last_name)
                if builderFormForEventRegistrationsCSV.cleaned_data['emergency_contact_relationship']:
                    row.append(event_registration.emergency_contact_relationship)
                if builderFormForEventRegistrationsCSV.cleaned_data['emergency_contact_phone_number']:
                    row.append(event_registration.emergency_contact_phone_number)
                if builderFormForEventRegistrationsCSV.cleaned_data['paid']:
                    row.append(event_registration.paid)
                if builderFormForEventRegistrationsCSV.cleaned_data['bill_to']:
                    row.append(event_registration.bill_to)
                if builderFormForEventRegistrationsCSV.cleaned_data['billing_physical_address']:
                    row.append(event_registration.billing_physical_address)
                if builderFormForEventRegistrationsCSV.cleaned_data['billing_email_address']:
                    row.append(event_registration.billing_email_address)
                if builderFormForEventRegistrationsCSV.cleaned_data['admin_billing_comments']:
                    row.append(event_registration.admin_billing_comments)

                writer.writerow(row)

            return response

        else:
            messages.warning(request, 'Event registrations CSV builder form has an invalid field.')

    context = {
        'event': event,
        'event_pk': event.pk,
        'registrations_csv_builder_form': builderFormForEventRegistrationsCSV,
    }

    return render(request, 'events/event_management.html', context)


# TODO: add staff and admin permissions
@login_required
def generate_event_dietary_requirement_counts_csv(request, pk):
    """Generate a custom CSV of event dietary requirement counts data."""
    event = Event.objects.get(pk=pk)

    if not can_view_event_management_content(request, event):
        messages.warning(
            request,
            NON_EVENT_STAFF_ACCESS_MESSAGE.format(request.user.first_name, event.name)
        )
        return HttpResponseRedirect(reverse("events:events_management"))

    heading_row = ["event name", "dietary requirements", "counts"]

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="dietary_requirement_counts_for_{}.csv"'.format(
        event.name
    )

    # Create a csv writer
    writer = csv.writer(response)

    # Designate the model
    APPROVED = 2
    event_registrations = EventRegistration.objects.filter(event=event, status=APPROVED)

    # Add column headings to the csv file
    writer.writerow(heading_row)

    dietary_reqs_dict = dict()

    for registration in event_registrations:
        dietary_requirements = [dR.name for dR in registration.user.dietary_requirements.all()]
        if "Give me coffee and no-one gets hurt" in dietary_requirements:
            dietary_requirements.remove("Give me coffee and no-one gets hurt")

        if frozenset(dietary_requirements) in dietary_reqs_dict:
            dietary_reqs_dict[frozenset(dietary_requirements)] += 1
        else:
            dietary_reqs_dict[frozenset(dietary_requirements)] = 1

    row_lists = [
        [
            event.name, convertStringListToOneString(list(frozenset_dietary_reqs)),
            dietary_reqs_dict[frozenset_dietary_reqs]
        ] for frozenset_dietary_reqs in dietary_reqs_dict.keys()
    ]

    for row in row_lists:
        writer.writerow(row)

    return response


# TODO: add staff and admin permissions
@login_required
def mark_all_participants_as_paid(request, pk):
    """Bulk mark all event registrations as being paid for for a given event."""
    event_id = pk
    event = Event.objects.get(id=event_id)
    event_registrations = [EventRegistration.objects.filter(event=event)]

    if not can_view_event_management_content(request, event):
        messages.warning(
            request,
            NON_EVENT_STAFF_ACCESS_MESSAGE.format(request.user.first_name, event.name)
        )
        return HttpResponseRedirect(reverse("events:events_management"))

    for event_registration in event_registrations:

        registration_to_update = EventRegistration.objects.filter(id=event_registration.id)
        registration_to_update.update(paid=True)
        registration_to_update = EventRegistration.objects.get(id=event_registration.id)
        registration_to_update.save()

    messages.success(
        request,
        f'You have marked all event registrations for \"{event.name}\" who have been approved as paid'
    )
    return redirect(reverse('events:event_management', kwargs={'pk': pk}))


# TODO: consider - add logic for checking if has close datetime for registrations
# make sure closing date for registration is on details page
# TODO: add logic for event detail page saying event registrations opening soon!
@login_required
def publish_event(request, pk):
    """Publish event as event staff."""
    event_id = pk
    event_query_set = Event.objects.filter(id=event_id)
    event = Event.objects.get(id=event_id)

    if not can_view_event_management_content(request, event):
        messages.warning(
            request,
            NON_EVENT_STAFF_ACCESS_MESSAGE.format(request.user.first_name, event.name)
        )
        return HttpResponseRedirect(reverse("events:events_management"))

    if (
        (event.published is False and event.start is None)
        or (event.published is False and event.end is None)
    ):
        messages.error(request, 'Your event must have a start and end datetime to be published.')
    elif (
        (event.published is False and event.registration_form.open_datetime is None)
        or (event.published is False and event.registration_form.close_datetime is None)
    ):
        messages.error(
            request,
            'Your event must have datetimes for when its registrations open and close before it is published.'
        )
    else:
        event_query_set.update(published=True)
        updated_event = Event.objects.get(id=event_id)
        updated_event.save()
        messages.success(request, 'Your event has been published!')
    return redirect(reverse('events:event_management', kwargs={'pk': pk}))


@login_required
def cancel_event(request, pk):
    """Cancel event as event staff."""
    event_id = pk
    event = Event.objects.filter(id=event_id)

    event_obj = Event.objects.get(pk=event_id)
    if not can_view_event_management_content(request, event_obj):
        messages.warning(
            request,
            NON_EVENT_STAFF_ACCESS_MESSAGE.format(request.user.first_name, event.name)
        )
        return HttpResponseRedirect(reverse("events:events_management"))

    event.update(is_cancelled=True)
    updated_event = Event.objects.get(id=event_id)
    updated_event.save()
    messages.success(request, 'Your event has been cancelled')
    return redirect(reverse('events:event_management', kwargs={'pk': pk}))


@login_required
def create_new_participant_type(request, pk):
    """Cancel event as event staff."""
    event = Event.objects.get(pk=pk)

    if not can_view_event_management_content(request, event):
        messages.warning(
            request,
            NON_EVENT_STAFF_ACCESS_MESSAGE.format(request.user.first_name, event.name)
        )
        return HttpResponseRedirect(reverse("events:events_management"))

    if request.method == 'POST':
        participant_type_creation_form = ParticipantTypeCreationForm(request.POST)

        if participant_type_creation_form.is_valid():
            name = participant_type_creation_form.cleaned_data['name']
            price = participant_type_creation_form.cleaned_data['price']

            if ParticipantType.objects.filter(name=name, price=price).exists():
                # participant type exists in general
                if ParticipantType.objects.filter(name=name, price=price, events=event).exists():
                    # participant type already exists for this event
                    participant_type = ParticipantType.objects.create(name=name, price=price)
                    messages.warning(
                        request,
                        f"The participant type {participant_type} already exists for this event."
                    )
                else:
                    # participant type does exist but is not associated with this event yet
                    existing_participant_type = ParticipantType.objects.get(name=name, price=price)
                    event.participant_types.add(existing_participant_type)
                    event.save()
                    existing_participant_type.save()
                    messages.success(
                        request,
                        f"The participant type {existing_participant_type} has been created."
                    )
            else:
                # participant doesn't exist yet in general
                new_participant_type = ParticipantType.objects.create(name=name, price=price)
                event.participant_types.add(new_participant_type)
                event.save()
                new_participant_type.save()
                messages.success(
                    request,
                    "The participant type " + str(new_participant_type) + " has been created."
                )

        else:
            messages.error(
                request,
                "The participant type was unable to be created since the price was not in the format of $1.23."
            )

        context = {
            'new_participant_form': participant_type_creation_form
            }
        # return render(request, 'events/event_management.html', context)

    return redirect(reverse('events:event_management', kwargs={'pk': pk}), context)


@login_required
def update_participant_type(request, event_pk, participant_type_pk):
    """Update event participant type.

    Note that we cannot immediately update this specific participant as it may be being used for other events as well.
    """
    event = Event.objects.get(pk=event_pk)
    old_participant_type = ParticipantType.objects.get(pk=participant_type_pk)

    if not can_view_event_management_content(request, event):
        messages.warning(
            request,
            NON_EVENT_STAFF_ACCESS_MESSAGE.format(request.user.first_name, event.name)
        )
        return HttpResponseRedirect(reverse("events:events_management"))

    # check if participant used by other events
    if Event.objects.filter(participant_types=participant_type_pk).count() > 1:
        # participant used by other events so just remove this event from the list
        old_participant_type.events.remove(event)
        old_participant_type.save()
    else:
        old_participant_type.delete()

    # check if new participant type already exists
    if ParticipantType.objects.filter(name=request.POST['name'], price=request.POST['price']).exists():
        # add the event to the list of events that use the existing "new" participant type
        new_participant_type = ParticipantType.objects.get(name=request.POST['name'], price=request.POST['price'])
        new_participant_type.events.add(event)
        new_participant_type.save()
    else:
        # "update" participant by creating new participant type
        new_participant_type = ParticipantType.objects.create(name=request.POST['name'], price=request.POST['price'])
        new_participant_type.events.add(event)
        new_participant_type.save()

    messages.success(
        request,
        f"You have updated the participant type of {old_participant_type} " +
        f"to {new_participant_type}."
    )

    return HttpResponseRedirect(reverse("events:event_management", kwargs={'pk': event.pk}))


@login_required
def delete_participant_type(request, event_pk, participant_type_pk):
    """Delete event participant type.

    We cannot immediately delete this specific participant as it may be being used for other events as well.
    """
    event = Event.objects.get(pk=event_pk)
    participant_type = get_object_or_404(ParticipantType, id=participant_type_pk)

    if not can_view_event_management_content(request, event):
        messages.warning(
            request,
            NON_EVENT_STAFF_ACCESS_MESSAGE.format(request.user.first_name, event.name)
        )
        return HttpResponseRedirect(reverse("events:events_management"))

    if Event.objects.filter(participant_types=participant_type_pk).count() == 1:
        participant_type.delete()
        event.save()
    else:
        # participant used by other events so just remove this event from the list
        event.participant_types.remove(participant_type)
        event.save()
        participant_type.save()

    messages.success(
        request,
        f'You have deleted the participant type of {participant_type})'
    )
    return HttpResponseRedirect(reverse("events:event_management", kwargs={'pk': event.pk}))


MESSAGE_TEMPLATE = "{message}\n\n-----\nMessage sent from {user} ({email})"


@login_required
def email_participants(request, event_pk):
    """Send bulk email to all event participants as event staff."""
    event = Event.objects.get(pk=event_pk)
    if not can_view_event_management_content(request, event):
        messages.warning(
            request,
            NON_EVENT_STAFF_ACCESS_MESSAGE.format(request.user.first_name, event.name)
        )
        return HttpResponseRedirect(reverse("events:events_management"))

    user = request.user

    if request.method == 'POST':
        contact_participants_form = ContactParticipantsForm(
            request.POST,
            initial={
                'from_email': event.contact_email_address,
                'name': user,
                }
            )
        if contact_participants_form.is_valid():
            subject = contact_participants_form.cleaned_data['subject']
            from_email = contact_participants_form.cleaned_data['from_email']
            message = MESSAGE_TEMPLATE.format(
                message=contact_participants_form.cleaned_data['message'],
                user=contact_participants_form.cleaned_data['name'],
                email=from_email
            )

            send_to_emails = []

            if contact_participants_form.cleaned_data['cc_sender'] is True:
                send_to_emails += [from_email]

            approved_status = 2
            pending_status = 1

            custom_message = "event participant"

            if (contact_participants_form.cleaned_data['send_to_approved_participants'] is True):
                registrations = EventRegistration.objects.filter(event=event, status=approved_status)
                participants = [registration.user for registration in registrations]
                send_to_emails += [participant.email for participant in participants]
                custom_message = "approved event participant"
            if (contact_participants_form.cleaned_data['send_to_pending_applicants'] is True):
                registrations = EventRegistration.objects.filter(event=event, status=pending_status)
                participants = [registration.user for registration in registrations]
                send_to_emails += [participant.email for participant in participants]
                custom_message = "pending event participant"
            if (
                contact_participants_form.cleaned_data['send_to_approved_participants'] is True and
                contact_participants_form.cleaned_data['send_to_pending_applicants'] is True
               ):
                custom_message = "event participant"

            total_participants = len(send_to_emails)

            if total_participants > 0:
                for email_address in send_to_emails:
                    send_mail(
                        subject,
                        message,
                        from_email,
                        [email_address],
                        fail_silently=False,
                    )
                if total_participants > 1:
                    messages.success(
                        request,
                        f"You have sent an email to all {total_participants} {custom_message}s"
                    )
                else:
                    messages.success(
                        request,
                        f"You have sent an email to {total_participants} {custom_message}"
                    )
                return HttpResponseRedirect(reverse("events:event_management", kwargs={'pk': event_pk}))

            else:
                messages.success(request, "There are no event participants to email yet for this event.")
        else:
            messages.warning(
                request,
                'Email could not be sent. You must choose to send your email to either or both groups of participants.'
                )

    event = Event.objects.get(pk=event_pk)
    context = {
        'event': event,
        'event_pk': event_pk,
    }
    registration_form = event.registration_form
    event_registrations = EventRegistration.objects.filter(event=event)
    context['manage_event_details_form'] = ManageEventDetailsForm(instance=event)
    context['manage_registration_form_details_form'] = ManageEventRegistrationFormDetailsForm(
        instance=registration_form
        )
    context['registrations_csv_builder_form'] = BuilderFormForEventRegistrationsCSV()
    context['event_registrations'] = event_registrations
    context['registration_form_pk'] = registration_form.pk
    context['is_free'] = event.is_free
    context['participant_types'] = ParticipantType.objects.filter(events=event).order_by('-price', 'name')
    # context['new_participant_form'] = ParticipantTypeCreationForm()
    # context['update_participant_form'] = ParticipantTypeCreationForm()
    context['contact_participants_form'] = contact_participants_form
    # use the existing form in order to load the valid inputs in the form whilst showing errors

    return render(request, 'events/event_management.html', context)
