from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import (CreateView, DetailView, ListView,
                                  TemplateView, UpdateView)

from events.forms import TicketForm
from events.models import Event, Ticket


class Overview(ListView):
    template_name = 'events/overview.html'
    model = Event
    context_object_name = 'events'
    ordering = ['date', 'time']


class EventDetailView(DetailView):
    model = Event


class TicketListView(PermissionRequiredMixin, ListView):
    model = Ticket
    permission_required = ('admin',)
    context_object_name = 'tickets'


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
    form_class = TicketForm
    permission_required = ('admin',)
    extra_context = {'update_form': True}

    def get_success_message(self, cleaned_data):
        return f'{self.object} {_("has been edited successfully.")}'

    def get_success_url(self):
        return reverse('calendar:tickets-all')
