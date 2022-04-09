from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, ListView, TemplateView, UpdateView

from payments.forms import PaymentForm
from payments.models import Payment


class Overview(PermissionRequiredMixin, CreateView):
    model = Payment
    form_class = PaymentForm
    permission_required = ('admin',)
    template_name = 'payments/payment_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'payments': Payment.objects.all()})
        return context

    def get_success_message(self, cleaned_data):
        return f'{self.object} {_("has been created successfully.")}'

    def get_success_url(self):
        return reverse('payments:all')


class PaymentCreateView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Payment
    form_class = PaymentForm
    permission_required = ('admin',)

    def get_success_message(self, cleaned_data):
        return f'{self.object} {_("has been created successfully.")}'

    def get_success_url(self):
        return reverse('payments:all')


class PaymentUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Payment
    form_class = PaymentForm
    permission_required = ('admin',)
    extra_context = {'update_form': True}

    def get_success_message(self, cleaned_data):
        return f'{self.object} {_("has been edited successfully.")}'

    def get_success_url(self):
        return reverse('payments:all')
