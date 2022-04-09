from django import forms

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
