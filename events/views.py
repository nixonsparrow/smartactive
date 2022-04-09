from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from events.forms import TicketForm, TicketUpdateForm
from events.models import Event, Ticket


class Overview(ListView):
    template_name = 'events/overview.html'
    model = Event
    context_object_name = 'events'
    ordering = ['date', 'time']

    def post(self, request, *args, **kwargs):
        direction = request.POST.get('direction')
        event = Event.objects.get(id=request.POST.get('event'))
        user = self.request.user

        if direction == 'IN':
            user.register_on_event(event)
        elif direction == 'OUT':
            user.unregister_from_event(event)
        else:
            pass

        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('calendar:overview')


class EventDetailView(DetailView):
    model = Event


class TicketListView(PermissionRequiredMixin, CreateView):
    model = Ticket
    form_class = TicketForm
    permission_required = ('admin',)
    template_name = 'events/ticket_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'tickets': Ticket.objects.all()})
        return context

    def get_success_message(self, cleaned_data):
        return f'{self.object} {_("has been created successfully.")}'

    def get_success_url(self):
        return reverse('calendar:tickets-all')


class TicketCreateView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Ticket
    form_class = TicketForm
    permission_required = ('admin',)

    def get_success_message(self, cleaned_data):
        return f'{self.object} {_("has been created successfully.")}'

    def get_success_url(self):
        return reverse('calendar:tickets-all')


class TicketUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Ticket
    form_class = TicketUpdateForm
    permission_required = ('admin',)
    extra_context = {'update_form': True}

    def get_success_message(self, cleaned_data):
        return f'{self.object} {_("has been edited successfully.")}'

    def get_success_url(self):
        return reverse('calendar:tickets-all')
