import datetime

from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from users.models import User


class Type(models.Model):
    class Meta:
        verbose_name = _('Type')
        verbose_name_plural = _('Types')

    name = models.CharField(_('Name'), default='', null=False, blank=False, max_length=50)


class EventSchema(models.Model):
    class Meta:
        verbose_name = _('Event schema')
        verbose_name_plural = _('Events schemas')

    WEEKDAYS = [
        (1, _('Monday')),
        (2, _('Tuesday')),
        (3, _('Wednesday')),
        (4, _('Thursday')),
        (5, _('Friday')),
        (6, _('Saturday')),
        (7, _('Sunday')),
    ]

    title = models.CharField(_('Title'), max_length=50, default='', null=False, blank=False)
    type = models.ForeignKey(Type, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    weekday = models.IntegerField(_('Weekday'), choices=WEEKDAYS, default=None, null=False, blank=False)
    time = models.TimeField(_('Time'), default=datetime.time(hour=18, minute=00), null=False)
    date_from = models.DateField(_('Date from'), default=now, null=False)
    date_to = models.DateField(_('Date to'), default=now, null=False)
    participants_limit = models.IntegerField(_('Limit of participants'), default=10)


class Event(models.Model):
    class Meta:
        verbose_name = _('Event')
        verbose_name_plural = _('Events')

    title = models.CharField(_('Title'), default='', null=False, blank=False, max_length=50)
    type = models.ForeignKey(Type, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    time = models.TimeField(_('Time'), default=datetime.time(hour=18, minute=00), null=False)
    date = models.DateField(_('Date'), default=now)
    trainer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                verbose_name=_('Trainer'), related_name='events_as_trainer')
    participants = models.ManyToManyField(User, verbose_name=_('Participants'), related_name='events_as_participant')
    schema = models.ForeignKey(EventSchema, on_delete=models.SET_NULL, null=True, blank=True,
                               verbose_name=_('Schema'), related_name='events')
    participants_limit = models.IntegerField(_('Limit of participants'), default=10)
