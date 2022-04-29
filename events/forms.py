from django import forms

from events.models import Event
from payments.models import Ticket


class TicketForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Ticket
        fields = ['user', 'event_type', 'usages_left']


class TicketUpdateForm(TicketForm):
    class Meta:
        model = Ticket
        fields = TicketForm.Meta.fields + ['active']


class EventForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Event
        fields = ['title', 'type', 'short_description', 'description', 'date', 'time',
                  'trainer', 'participants', 'schema',
                  'participants_limit', 'register_time_limit', 'unregister_time_limit']
