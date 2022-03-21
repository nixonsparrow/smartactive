from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from payments.przelewy24 import przelewy


class Overview(TemplateView):
    template_name = 'payments/payment.html'

    def post(self):
        przelewy()
