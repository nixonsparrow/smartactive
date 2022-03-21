from django.views.generic import TemplateView

from payments.models import Payment


class Overview(TemplateView):
    template_name = 'payments/overview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['payments'] = Payment.objects.all()
        return context
