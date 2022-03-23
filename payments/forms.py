from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from events.models import Type
from payments.models import Payment


class PaymentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Payment
        fields = ['user', 'amount', 'initial_usages', 'event_type']
