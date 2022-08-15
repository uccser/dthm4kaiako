"""Views for events application."""

import re
from django.views import generic
from django.utils.timezone import now
from django_filters.views import FilterView
from utils.mixins import RedirectToCosmeticURLMixin
from events.models import (
    DeletedEventApplication,
    Event,
    Location,
    EventApplication,
    Address,
    RegistrationForm
)
from users.models import ( User )
from events.filters import UpcomingEventFilter, PastEventFilter
from events.utils import create_filter_helper, organise_schedule_data
from .forms import (EventApplicationForm,
                    TermsAndConditionsForm, 
                    BillingDetailsForm, 
                    WithdrawEventApplicationForm, 
                    ManageEventApplicationForm, 
                    ManageEventDetailsForm,
                    ManageEventRegistrationFormDetailsForm,
                    ManageEventLocationForm,
                    )
from django.shortcuts import render, redirect
from users.forms import UserUpdateDetailsForm
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import formset_factory
from django.core.exceptions import ValidationError
import csv

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

    def get_application_pk(self, user):
        """Returns the primary key of the user's event application of the event."""

        event_application_pk = 0
        if EventApplication.objects.filter(event=self.object.pk, user=user).exists():
            event_application = EventApplication.objects.get(event=self.object.pk, user=user)
            event_application_pk = event_application.pk
        return event_application_pk


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
        withdraw_event_application_form = WithdrawEventApplicationForm(self.request.POST)

        if user.is_authenticated:
            context['has_user_applied'] = self.does_application_exist(user)
            context['application_pk'] = self.get_application_pk(user)
        else:
            context['user_is_authenticated'] = False

        context['withdraw_event_application_form'] = withdraw_event_application_form
        
        return context


class LocationDetailView(RedirectToCosmeticURLMixin, generic.DetailView):
    """View for a specific location."""

    model = Location
    context_object_name = 'location'


class EventApplicationsView(LoginRequiredMixin, generic.ListView):
    """View for listing all a user's event applications."""

    template_name = 'events/event_applications.html'
    model = EventApplication

    
    def get_context_data(self, **kwargs):
        """Provide the context data for the event applictions view.

        Returns:
            Dictionary of context data.
        """
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.is_authenticated:
            unordered_event_applications = EventApplication.objects.filter(user=user).order_by(
                'event__start')
            context['event_applications'] = unordered_event_applications
            context['user'] = self.request.user
            context['withdraw_event_application_form'] = WithdrawEventApplicationForm(self.request.POST)
        return context

    def get_object(self):
        """Retrieve the user object for the associated template."""
        return self.request.user


@login_required
def delete_application_via_application_page(request, pk):
    """ Allowing a user to delete an existing event application from their event applications page."""

    event_application = get_object_or_404(EventApplication, pk=pk)
    event = Event.objects.get(pk=event_application.event.pk)

    if request.method == 'POST':
        create_deleted_event_application(event, request)
        event_application.delete()
        messages.success(request, 'Event application successfully withdrawn')
        return HttpResponseRedirect(reverse("events:event_applications"))

    return render(request, 'events/event_applications.html')


@login_required
def delete_application_via_event_page(request, pk):
    """ Allowing a user to delete an existing event application from their event applications page."""

    event_application = get_object_or_404(EventApplication, pk=pk)
    event = Event.objects.get(pk=event_application.event.pk)

    if request.method == 'POST':
        create_deleted_event_application(event, request)
        event_application.delete()
        messages.success(request, 'Event application successfully withdrawn')
        return HttpResponseRedirect(reverse("events:event", kwargs={'pk': event.pk, 'slug': event.slug}))

    return render(request, 'event_details.html')


def create_deleted_event_application(event, request):
    """
    Create and save DeletedEventApplication based on the retrieved deletion reason and/or other reason for deletion.
    """

    reason = request.POST['deletion_reason']
    deleted_event_application = DeletedEventApplication.objects.create(
    deletion_reason = reason,
    event = event
    )

    if reason == '7':
        # Other reason
        other_reason = request.POST['other_reason_for_deletion']
        deleted_event_application = DeletedEventApplication.objects.create(
            deletion_reason = reason,
            event = event,
            other_reason_for_deletion = other_reason
    )
    deleted_event_application.save()


def validate_event_application_form(event_application_form, 
                                    user_update_details_form, 
                                    terms_and_conditions_form, 
                                    billing_required, 
                                    billing_details_form,
                                    ):
    """
    Validates that the event application is valid.
    Also accommodates for the billing section and dietary requirements sections to be only validated if they are needed i.e. are rended.
    """

    if event_application_form.is_valid() and user_update_details_form.is_valid() and terms_and_conditions_form.is_valid() and (not billing_required or billing_details_form.is_valid()):
        return True
    else:
        return False


def does_application_exist(user, event):
    """
    Returns True if event application already exists for the given user and event.
    """
    return user.event_applications.filter(event=event).exists()


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
    billing_details_form = None
    terms_and_conditions_form = None
    billing_required = not event.is_free
    display_catering_info = event.is_catered
    initial_user_data={'show_dietary_requirements': event.is_catered, 
                    'show_medical_notes': not event.accessible_online
                    }
    initial_event_application_data={'show_emergency_contact_fields': not event.accessible_online}
    new_billing_email = None
    current_application = None
    billing_physical_address = None
    billing_email_address = ""
    bill_to = ""

    if request.method == 'GET':
        # Prior to creating/updating registration form

        if does_application_exist(user, event):
            current_application = user.event_applications.get(event=event)
            event_application_form = EventApplicationForm(instance=current_application, initial=initial_event_application_data)
            billing_physical_address = current_application.billing_physical_address
            billing_email_address = current_application.billing_email_address
            bill_to = current_application.bill_to
            initial_user_data={'show_dietary_requirements': event.is_catered, 
                            'show_medical_notes': not event.accessible_online,
                            'mobile_phone_number': user.mobile_phone_number,
                            'email_address': user.email_address}
        else:
            event_application_form = EventApplicationForm(initial=initial_event_application_data)
        
        user_update_details_form = UserUpdateDetailsForm(instance=user, initial=initial_user_data) # autoload existing event application's user data
        if billing_required:
            initial_billing_data = {'billing_email_address': billing_email_address, 'bill_to': bill_to}
            billing_details_form = BillingDetailsForm(instance=billing_physical_address, initial=initial_billing_data) # TODO: figure out how to autoload billing info
        terms_and_conditions_form = TermsAndConditionsForm(
                initial={'I_agree_to_the_terms_and_conditions': False,
                } # User must re-agree each time they update the form
            )

        
        if event.is_less_than_one_week_prior_event and event.is_catered:
            messages.warning(request, f'Your dietary requirements may not be considered for catering due to it being too close to the event commencing. Please consider contacting us at {event.contact_email_address}')
    

    elif request.method == 'POST':
        # If creating a new application or updating existing application (as Django forms don't support PUT)
        
        user_update_details_form = UserUpdateDetailsForm(request.POST, instance=user, initial=initial_user_data)

        if does_application_exist(user, event):
            current_application = user.event_applications.get(event=event)
            event_application_form = EventApplicationForm(request.POST, instance=current_application)
        else:
            event_application_form = EventApplicationForm(request.POST)

        if billing_required:
            initial_billing_data = {'billing_email_address': billing_email_address, 'bill_to': bill_to}
            billing_details_form = BillingDetailsForm(request.POST, initial=initial_billing_data)
        terms_and_conditions_form = TermsAndConditionsForm(request.POST)


        if validate_event_application_form(event_application_form, 
                                    user_update_details_form, 
                                    terms_and_conditions_form, 
                                    billing_required, 
                                    billing_details_form,
                                    ):                  
            user.first_name = user_update_details_form.cleaned_data['first_name']
            user.last_name = user_update_details_form.cleaned_data['last_name']
            all_educational_entities = user_update_details_form.cleaned_data['educational_entities']
            user.educational_entities.set(all_educational_entities)
            user.region = user_update_details_form.cleaned_data['region']
            user.email_address = user_update_details_form.cleaned_data['email_address']
            user.mobile_phone_number = user_update_details_form.cleaned_data['mobile_phone_number']

            if event.accessible_online:
                user.medical_notes = user_update_details_form.cleaned_data['medical_notes']

            if display_catering_info:
                all_dietary_reqs = user_update_details_form.cleaned_data['dietary_requirements']
                user.dietary_requirements.set(all_dietary_reqs)
            user.save()

            new_participant_type = event_application_form.cleaned_data['participant_type']
            new_representing = event_application_form.cleaned_data['representing']
            new_emergency_contact_first_name = event_application_form.cleaned_data['emergency_contact_first_name']
            new_emergency_contact_last_name = event_application_form.cleaned_data['emergency_contact_last_name']
            new_emergency_contact_relationship = event_application_form.cleaned_data['emergency_contact_relationship']
            new_emergency_contact_phone_number = event_application_form.cleaned_data['emergency_contact_phone_number']

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

                event_application, created = EventApplication.objects.update_or_create(
                    user=user, event=event,
                    defaults={
                        'participant_type': new_participant_type,
                        'representing': new_representing,
                        'billing_physical_address': new_billing_address,
                        'billing_email_address': new_billing_email,
                        'emergency_contact_first_name': new_emergency_contact_first_name,
                        'emergency_contact_last_name': new_emergency_contact_last_name,
                        'emergency_contact_relationship': new_emergency_contact_relationship,
                        'emergency_contact_phone_number': new_emergency_contact_phone_number,
                        'bill_to': new_bill_to,
                    }
                )
                event_application.save()
            
            else:
                event_application, created = EventApplication.objects.update_or_create(
                user=user, event=event,
                defaults={
                    'participant_type': new_participant_type,
                    'representing': new_representing,
                    'emergency_contact_first_name': new_emergency_contact_first_name,
                    'emergency_contact_last_name': new_emergency_contact_last_name,
                    'emergency_contact_relationship': new_emergency_contact_relationship,
                    'emergency_contact_phone_number': new_emergency_contact_phone_number,
                    'bill_to': new_bill_to,
                }
            )
            event_application.save()
            

            if does_application_exist(user, event):
                # Update existing event application
                messages.success(request, "Updated event application successfully")
                return HttpResponseRedirect(reverse("events:event", kwargs={'pk': event.pk, 'slug': event.slug})) # Return to event detail page

            else:
                # Create new event application
                messages.success(request, 'New event application created successfully')
                return HttpResponseRedirect(reverse("events:event", kwargs={'pk': event.pk, 'slug': event.slug})) # Return to event detail page


    context = {
        'event': event,
        'event_application_form': event_application_form,
        'user_form': user_update_details_form,
        'billing_details_form': billing_details_form,
        'billing_required': billing_required,
        'terms_and_conditions_form': terms_and_conditions_form,
        'withdraw_event_application_form': WithdrawEventApplicationForm(request.POST)
    }

    return render(request, 'events/apply.html', context)


class EventsManagementHubView(LoginRequiredMixin, generic.ListView):
    """View for a events management."""

    template_name = 'events/events_management_hub.html'

    def get_context_data(self, **kwargs):
        """Provide the context data for the events management view.

        Returns:
            Dictionary of context data.
        """
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.is_authenticated:
            if Event.objects.filter(event_staff=user.pk).exists():
                context['events_user_is_staff_for'] = [Event.objects.get(event_staff=user.pk)]
            else:
                context['events_user_is_staff_for'] = []
  
        return context


    def get_queryset(self):
        """Show all events.

        Returns:
            Events.
        """
        return Event.objects.all()


@login_required
def manage_event(request, pk):
    """
    View for event management. 
    Contains form sets for each event related object (similar to that in Admin app).
    These can be viewed, updated (based on non-read only fields) and deleted.
    """
    """
    View for event management. 
    Contains form sets for each event related object (similar to that in Admin app).
    These can be viewed, updated (based on non-read only fields) and deleted.
    """

    event = Event.objects.get(pk=pk)
    user = request.user
    event_applications = EventApplication.objects.filter(event=event)
    registration_form = event.registration_form
    context = {
        'event': event,
    }
    event_applications_formset = None
    EventApplicationFormSet = None
    manage_event_details_form = None
    manage_registration_form_details_form = None
    manage_location_form = None

    if len(event_applications) == 0:
        return render(request, 'events/event_management.html', context)
    else:
        initial_for_event_applications_formset = [
                                                    {
                                                        'submitted': event_application.submitted,
                                                        'updated': event_application.updated,
                                                        'status': event_application.status,
                                                        'participant_type': event_application.participant_type,
                                                        'staff_comments': event_application.staff_comments,
                                                        'representing': event_application.representing,
                                                        'event': event_application.event,
                                                        'emergency_contact_first_name': event_application.emergency_contact_first_name,
                                                        'emergency_contact_last_name': event_application.emergency_contact_last_name,
                                                        'emergency_contact_relationship': event_application.emergency_contact_relationship,
                                                        'emergency_contact_phone_number': event_application.emergency_contact_phone_number,
                                                        'paid': event_application.paid,
                                                        'bill_to': event_application.bill_to,
                                                        'billing_physical_address': event_application.billing_physical_address,
                                                        'billing_email_address': event_application.billing_email_address, 
                                                        'participant_first_name': event_application.user.first_name,
                                                        'participant_last_name': event_application.user.last_name,
                                                        'participant_region_name': event_application.user.region,
                                                        # 'educational_entities': event_application.user.educational_entities,
                                                        # 'dietary_requirements': event_application.user.dietary_requirements,
                                                        'medical_notes': event_application.user.medical_notes,
                                                        'email_address': event_application.user.email_address,
                                                        'mobile_phone_number': event_application.user.mobile_phone_number,
                                                    } for event_application in event_applications
                                                ] 
        data = {
            'form-TOTAL_FORMS': len(event_applications),
            'form-INITIAL_FORMS': len(event_applications),
        }  

        EventApplicationFormSet = formset_factory(ManageEventApplicationForm, extra=0)

        if request.method == 'GET':
            event_applications_formset = EventApplicationFormSet(data, initial=initial_for_event_applications_formset)
            manage_event_details_form = ManageEventDetailsForm(instance=event)
            manage_registration_form_details_form = ManageEventRegistrationFormDetailsForm(instance=registration_form)
            
            #TODO: add in formset for location: manage_location_form = ManageEventLocationForm(instance=location)


        elif request.method == 'POST':
            event_applications_formset = EventApplicationFormSet(data, request.POST, initial=initial_for_event_applications_formset)
            if event_applications_formset and event_applications_formset.is_valid():
                for form in event_applications_formset:
                    if form.cleaned_data:

                        messages.success(request, f"cleaned data: {form.cleaned_data}")
                        
                        # event_application = form.save(commit=False)

                        # updated_status = form.cleaned_data['status']

                        messages.success(request, f"participant_type: {form.cleaned_data['participant_type']}")
                        messages.success(request, f"staff_comments: {form.cleaned_data['staff_comments']}")
                        messages.success(request, f"paid: {form.cleaned_data['paid']}")

                        updated_participant_type = form.cleaned_data['participant_type']
                        updated_staff_comments = form.cleaned_data['staff_comments']
                        updated_paid_status = form.cleaned_data['paid']
                        event_application, created = EventApplication.objects.update_or_create(
                            user=user, event=event,
                            defaults={
                                # 'status': updated_status,
                                'participant_type': updated_participant_type,
                                'staff_comments': updated_staff_comments,
                                'paid': updated_paid_status,
                            }
                        )
                        event_application.save()                    
                        messages.success(request, 'Event application updated successfully')

                return HttpResponseRedirect(reverse("events:event_management", kwargs={'pk': event.pk,}))

            else:
                messages.success(request, 'Formset not present or invalid!')

        context['formset_applications'] = event_applications_formset
        context['manage_event_details_form'] = manage_event_details_form
        context['manage_registration_form_details_form'] = manage_registration_form_details_form
        context['event_pk'] = event.pk
        context['registration_form_pk'] = registration_form.pk
        context['is_free'] = event.is_free
        return render(request, 'events/event_management.html', context)


# TODO: add event staff access only
@login_required
def manage_event_details(request, pk):
    """ Allowing event staff to update event details as well as deleting the event if desired."""

    event = Event.objects.get(pk=pk)
    context = {
        'event': event,
    }

    if request.method == 'POST':
        manage_event_details_form = ManageEventDetailsForm(request.POST, instance=event, prefix="event_details")
        if manage_event_details_form.is_valid():

            updated_name = manage_event_details_form.cleaned_data['name']
            updated_description = manage_event_details_form.cleaned_data['description']
            updated_published = manage_event_details_form.cleaned_data['published']
            updated_show_schedule = manage_event_details_form.cleaned_data['show_schedule']
            updated_featured = manage_event_details_form.cleaned_data['featured']
            updated_registration_type = manage_event_details_form.cleaned_data['registration_type']
            updated_registration_link = manage_event_details_form.cleaned_data['registration_link']
            updated_start = manage_event_details_form.cleaned_data['start']
            updated_end = manage_event_details_form.cleaned_data['end']
            updated_accessible_online = manage_event_details_form.cleaned_data['accessible_online']
            updated_is_free = manage_event_details_form.cleaned_data['is_free'] #TODO: needs updating as this is calculated based on participant type costs.
            update_is_catered = manage_event_details_form.cleaned_data['is_catered']
            update_contact_email_address = manage_event_details_form.cleaned_data['contact_email_address']
            update_series = manage_event_details_form.cleaned_data['series']

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

            #TODO: update otherside of M2M relationships for locations, sponsors, organisers, serieses and event staff!

            Event.objects.filter(id=event.pk).update(
                name=updated_name,
                description=updated_description,
                published=updated_published,
                show_schedule=updated_show_schedule,
                featured=updated_featured,
                registration_type=updated_registration_type,
                registration_link=updated_registration_link,
                start=updated_start,
                end=updated_end,
                accessible_online=updated_accessible_online,
                is_free=updated_is_free,
                is_catered=update_is_catered,
                contact_email_address=update_contact_email_address,
                series=update_series,
            )
            event.save() 
            messages.success(request, 'Event details updated successfully')
            return HttpResponseRedirect(reverse("events:event_management", kwargs={'pk': event.pk}))
        else:
            messages.warning(request, 'Event details could not be updated. Please resolve invalid fields.')

    elif request.method == 'DELETE':
        event.delete()
        messages.success(request, 'Event deleted successfully')
        return HttpResponseRedirect(reverse("events:event_management", kwargs={'pk': event.pk}))

    context['manage_event_details_form'] = manage_event_details_form
    context['event'] = event
    context['event_pk'] = event.pk

    return render(request, 'events/event_management.html', context)


# TODO: add event staff access only
@login_required
def manage_event_registration_form_details(request, pk):
    """ Allowing event staff to update event registration form details.
    
    Note that registration_form is the RegistrationForm object (as per the model) and 
    registration_form_details_form is a Form object (for UI).
    
    """

    registration_form = RegistrationForm.objects.get(pk=pk)
    event = registration_form.event
    context = {
        'registration_form': registration_form,
    }

    if request.method == 'POST':
        manage_registration_form_details_form = ManageEventRegistrationFormDetailsForm(request.POST, instance=registration_form)
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
            messages.success(request, 'Event registration form details updated successfully')
            return HttpResponseRedirect(reverse("events:event_management", kwargs={'pk': event.pk}))
        else:
            messages.warning(request, 'Registration form details could not be updated. Please resolve invalid fields.')

    context['manage_registration_form_details_form'] = manage_registration_form_details_form
    context['event'] = event
    context['registration_form_pk'] = registration_form.pk

    return render(request, 'events/event_management.html', context)

# TODO: convert to location
# TODO: add event staff access only
@login_required
def manage_event_location_details(request, pk):
    """ Allowing event staff to update event location details.    
    """

    location = Location.objects.get(pk=pk)
    event = location.event #TODO: check this is correct
    context = {
        'location': location,
    }

    if request.method == 'POST':
        manage_location_form = ManageEventLocationForm(request.POST, instance=location)
        if manage_location_form.is_valid():

            updated_room = manage_location_form.cleaned_data['room']
            updated_name = manage_location_form.cleaned_data['name']
            updated_street_address = manage_location_form.cleaned_data['street_address']
            updated_suburb = manage_location_form.cleaned_data['suburb']
            updated_city = manage_location_form.cleaned_data['city']
            updated_region = manage_location_form.cleaned_data['region']
            updated_description = manage_location_form.cleaned_data['description']
            updated_coords = manage_location_form.cleaned_data['coords']

            Location.objects.filter(event_id=manage_location_form.pk).update(
                room=updated_room,
                name=updated_name,
                street_address=updated_street_address,
                suburb=updated_suburb,
                city=updated_city,
                region=updated_region,
                description=updated_description,
                coords=updated_coords,
            )
            location.save() 
            messages.success(request, 'Event location details updated successfully')
            return HttpResponseRedirect(reverse("events:event_management", kwargs={'pk': event.pk}))
        else:
            messages.warning(request, 'Location details could not be updated. Please resolve invalid fields.')

    context['manage_location_form'] = manage_location_form
    context['event'] = event
    context['location_pk'] = location.pk

    return render(request, 'events/event_management.html', context)

@login_required
def event_applications_csv(request, pk):
    '''Generates a CSV of all the event applications' data.'''

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] ='attachment; filename=event_applications.csv'

    # Create a csv writer
    writer = csv.writer(response)

    event = Event.objects.get(id=pk)

    # Designate the model
    event_applications = EventApplication.objects.filter(event=event)

    # Add column headings to the csv file
    writer.writerow(['Datetime Submitted', 
                        'Datetime updated', 
                        'Status', 
                        'Participant Type', 
                        'Staff Comments', 
                        'Participant Firstname', 
                        'Participant Lastname', 
                        'Representing', 
                        'Emergency Contact Firstname', 
                        'Emergency Contact Lastname', 
                        'Emergency Contact Relationship', 
                        'Emergency Contact Phone Number', 
                        'Paid Status', 
                        'Bill To', 
                        'Billing Physical Address', 
                        'Billing Email Address'
                    ])
    
    for event_application in event_applications:
        user = event_application.user
        # user = User.objects.filter(pk=user_pk)

        writer.writerow([event_application.submitted,
                            event_application.updated,
                            event_application.status,
                            event_application.participant_type,
                            event_application.staff_comments,
                            user.first_name,
                            user.last_name,
                            event_application.representing,
                            event_application.emergency_contact_first_name,
                            event_application.emergency_contact_last_name,
                            event_application.emergency_contact_relationship,
                            event_application.emergency_contact_phone_number,
                            event_application.paid,
                            event_application.bill_to,
                            event_application.billing_physical_address,
                            event_application.billing_email_address
        ])
    
    return response


@login_required
def participant_billing_details_csv(request, pk):
    '''Generates a CSV of all the event applications' data.'''

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] ='attachment; filename=participant_billing_details.csv'

    # Create a csv writer
    writer = csv.writer(response)

    event = Event.objects.get(id=pk)

    # Designate the model
    event_applications = EventApplication.objects.filter(event=event)

    # Add column headings to the csv file
    writer.writerow(['Participant Firstname', 
                        'Participant Lastname', 
                        'Representing',
                        'Paid Status', 
                        'Bill To',
                        'Billing Physical Address', 
                        'Billing Email Address'
                    ])
    
    for event_application in event_applications:
        user = event_application.user
        writer.writerow([
                            user.first_name,
                            user.last_name,
                            event_application.representing,
                            event_application.paid,
                            event_application.bill_to,
                            event_application.billing_physical_address,
                            event_application.billing_email_address
        ])
    
    return response


@login_required
def mark_all_participants_as_paid(request, pk):
    '''Bulk mark all event applications as being paid for for a given event.'''
    event_id = pk
    event = Event.objects.get(id=event_id)
    event_applications = EventApplication.objects.filter(event=event)

    for event_application in event_applications:

        application_to_update = EventApplication.objects.filter(id=event_application.id)
        application_to_update.update(paid=True)
        application_to_update = EventApplication.objects.get(id=event_application.id)
        application_to_update.save()
    
    messages.success(request, 'All event participants successfully marked as paid')
    return redirect(reverse('events:event_management', kwargs={'pk': pk}))

    