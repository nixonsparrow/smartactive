from django.shortcuts import render
from django.views.generic import DetailView, TemplateView

from events.models import Event


class Overview(TemplateView):
    template_name = 'events/overview.html'


class EventDetailView(DetailView):
    model = Event
