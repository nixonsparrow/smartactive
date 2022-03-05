from django.shortcuts import render
from django.views.generic import TemplateView


class Overview(TemplateView):
    template_name = 'events/overview.html'
