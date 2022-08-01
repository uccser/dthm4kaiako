"""Views for events application."""

from django.views import generic
from django.utils.timezone import now
from django_filters.views import FilterView
from utils.mixins import RedirectToCosmeticURLMixin
from events.models import (
    DeletedEventApplication,
    Event,
    Location,
    EventApplication,
    Address
)
from events.filters import UpcomingEventFilter, PastEventFilter
from events.utils import create_filter_helper, organise_schedule_data
from .forms import EventApplicationForm, TermsAndConditionsForm, BillingDetailsForm, WithdrawEventApplicationForm, ManageEventApplicationForm
from django.shortcuts import render
from users.forms import UserUpdateDetailsForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import formset_factory


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
            context['events_user_is_staff_for'] = [Event.objects.get(event_staff=user.pk)]
  
        return context


    def get_queryset(self):
        """Show all events.

        Returns:
            Events.
        """
        return Event.objects.all()


@login_required
def manage_event(request,pk):
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
    event_applications = EventApplication.objects.filter(event=event)

    context = {
        'event': event,
    }

    if len(event_applications) == 0:
        return render(request, 'events/event_management.html', context)
    else:

        # TODO: figure out how to uniquely initialise each form for each event application object
        # initial_for_event_applications_formset = [
        #                                             {'submitted': event_application.submitted,
        #                                                 'updated': event_application.updated,
        #                                                 'status': event_application.status,
        #                                                 'participant_type': event_application.participant_type,
        #                                                 'staff_comments': event_application.staff_comments,
        #                                                 'representing': event_application.representing,
        #                                                 'event': event_application.event,
        #                                                 'emergency_contact_first_name': event_application.emergency_contact_first_name,
        #                                                 'emergency_contact_last_name': event_application.emergency_contact_last_name,
        #                                                 'emergency_contact_relationship': event_application.emergency_contact_relationship,
        #                                                 'emergency_contact_phone_number': event_application.emergency_contact_phone_number,
        #                                                 'paid': event_application.paid,
        #                                                 'bill_to': event_application.bill_to,
        #                                                 'billing_physical_address': event_application.billing_physical_address,
        #                                                 'billing_email_address': event_application.billing_email_address,
        #                                                 'form-TOTAL_FORMS': len(event_applications),
        #                                                 'form-INITIAL_FORMS': len(event_applications)                                                        
        #                                             } for event_application in event_applications
                                                    
        #                                         ]

        # data_for_event_applications_formset = {
        #     'form-TOTAL_FORMS': len(event_applications),
        #     'form-INITIAL_FORMS': len(event_applications),
        # }


        # initial_for_event_applications_formset = {'submitted': event_applications[0].submitted,
        #                                             'updated': event_applications[0].updated,
        #                                             'status': event_applications[0].status,
        #                                             'participant_type': event_applications[0].participant_type,
        #                                             'staff_comments': event_applications[0].staff_comments,
        #                                             'representing': event_applications[0].representing,
        #                                             'event': event_applications[0].event,
        #                                             'emergency_contact_first_name': event_applications[0].emergency_contact_first_name,
        #                                             'emergency_contact_last_name': event_applications[0].emergency_contact_last_name,
        #                                             'emergency_contact_relationship': event_applications[0].emergency_contact_relationship,
        #                                             'emergency_contact_phone_number': event_applications[0].emergency_contact_phone_number,
        #                                             'paid': event_applications[0].paid,
        #                                             'bill_to': event_applications[0].bill_to,
        #                                             'billing_physical_address': event_applications[0].billing_physical_address,
        #                                             'billing_email_address': event_applications[0].billing_email_address,
        #                                             'form-TOTAL_FORMS': 1,
        #                                             'form-INITIAL_FORMS': 1                                                        
        #                                         }

        initial_for_event_applications_formset = {
                                            # 'submitted': event_applications[0].submitted,
                                            # 'updated': event_applications[0].updated,
                                            'status': event_applications[0].status,
                                            # 'participant_type': event_applications[0].participant_type,
                                            # 'staff_comments': event_applications[0].staff_comments,
                                            # 'representing': event_applications[0].representing,
                                            # 'event': event_applications[0].event,
                                            # 'emergency_contact_first_name': event_applications[0].emergency_contact_first_name,
                                            # 'emergency_contact_last_name': event_applications[0].emergency_contact_last_name,
                                            # 'emergency_contact_relationship': event_applications[0].emergency_contact_relationship,
                                            # 'emergency_contact_phone_number': event_applications[0].emergency_contact_phone_number,
                                            # 'paid': event_applications[0].paid,
                                            # 'bill_to': event_applications[0].bill_to,
                                            # 'billing_physical_address': event_applications[0].billing_physical_address,
                                            # 'billing_email_address': event_applications[0].billing_email_address,
                                            # 'form-TOTAL_FORMS': 1,
                                            # 'form-INITIAL_FORMS': 1                                                        
                                        }   

        EventApplicationFormSet = formset_factory(ManageEventApplicationForm)
        event_applications_formset = EventApplicationFormSet(prefix='applications')    

        # EventApplicationFormSet = formset_factory(ManageEventApplicationForm, extra=len(event_applications))
        # event_applications_formset = EventApplicationFormSet(prefix='applications', initial=initial_for_event_applications_formset)

        # EventApplicationFormSet = formset_factory(ManageEventApplicationForm)
        # event_applications_formset = EventApplicationFormSet(prefix='applications')

        context['formset'] = event_applications_formset

        if request.method == 'GET':
            event_applications_formset = EventApplicationFormSet(prefix='applications')

        elif request.method == 'POST':
            event_applications_formset = EventApplicationFormSet(request.POST, prefix='applications')
            if event_applications_formset.is_valid():
                for form in event_applications_formset:
                    if form.cleaned_data:
                        pass
                        # TODO: grab cleaned data values, update object and save. Pull existing data first using save(commit=False) then update the new fields and save normally at end
                return HttpResponseRedirect(reverse("events:event_management", kwargs={'pk': event.pk,}))
            

        return render(request, 'events/event_management.html', {'event': event, 'formset' : event_applications_formset})
