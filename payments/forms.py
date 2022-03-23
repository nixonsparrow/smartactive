from django import forms
from django.core.exceptions import ValidationError

from events.models import Type
from payments.models import Payment


class PaymentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Payment
        fields = ['user', 'amount', 'initial_entries']
