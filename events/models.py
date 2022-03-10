from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _


class Type(models.Model):
    name = models.CharField(_('Name'), max_length=50, default='', null=False, blank=False)


class Event(models.Model):
    type = models.ForeignKey(Type, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    date = models.DateField(_('Date'), default=now)
