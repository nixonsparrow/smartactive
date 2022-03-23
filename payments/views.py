from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, TemplateView, UpdateView

from payments.forms import PaymentForm
from payments.models import Payment


class Overview(TemplateView):
    template_name = 'payments/overview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['payments'] = Payment.objects.all()
        return context


class PaymentCreateView(SuccessMessageMixin, CreateView):
    model = Payment
    form_class = PaymentForm

    def get_success_message(self, cleaned_data):
        return f'{self.object} {_("has been created successfully.")}'

    def get_success_url(self):
        return reverse('payments:overview')


class PaymentUpdateView(SuccessMessageMixin, UpdateView):
    model = Payment
    form_class = PaymentForm
    extra_context = {'update_form': True}

    def get_success_message(self, cleaned_data):
        return f'{self.object} {_("has been edited successfully.")}'

    def get_success_url(self):
        return reverse('payments:overview')
