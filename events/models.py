import datetime

from dateutil.utils import today
from django.db import models
from django.utils.translation import gettext_lazy as _

from events.exceptions import (NoValidTicketFound, ParticipantsFull,
                               RegisterTimePassed, UnregisterTimePassed,
                               UserInParticipants, UserNotInParticipants)
from manager.models import TimestampedModel
from users.models import User


def tomorrow():
    return today() + datetime.timedelta(days=1)


class Type(models.Model):
    class Meta:
        verbose_name = _('Type')
        verbose_name_plural = _('Types')
        ordering = ['-id']

    name = models.CharField(_('Name'), default='', null=False, blank=False, max_length=50)

    def __str__(self):
        return self.name


class Ticket(TimestampedModel):
    class Meta:
        verbose_name = _('Ticket')
        verbose_name_plural = _('Tickets')
        ordering = ['-id']

    user = models.ForeignKey(User, verbose_name=_('User'), on_delete=models.SET_NULL,
                             null=True, blank=True, related_name='tickets')
    active = models.BooleanField(verbose_name=_('Active'), default=True)

    event_type = models.ForeignKey(Type, verbose_name=_('Type'), default=None, on_delete=models.SET_NULL,
                                   related_name='tickets', null=True, blank=False)
    usages_left = models.PositiveSmallIntegerField(verbose_name=_('Usages left'), default=1, null=False, blank=False)

    def __str__(self):
        return f'{_("Ticket")} ({self.id}): {self.user if self.user else _("Incognito")}'


class EventSchema(models.Model):
    class Meta:
        verbose_name = _('Event schema')
        verbose_name_plural = _('Events schemas')
        ordering = ['-id']

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
    subtitle = models.CharField(_('Subtitle'), max_length=50, default='', null=True, blank=True)
    type = models.ForeignKey(Type, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    weekday = models.IntegerField(_('Weekday'), choices=WEEKDAYS, default=None, null=False, blank=False)
    time = models.TimeField(_('Time'), default=datetime.time(hour=18, minute=00), null=False)
    date_from = models.DateField(_('Date from'), default=today, null=False)
    date_to = models.DateField(_('Date to'), default=tomorrow, null=False)
    participants_limit = models.IntegerField(_('Limit of participants'), default=10)


class Event(models.Model):
    class Meta:
        verbose_name = _('Event')
        verbose_name_plural = _('Events')
        ordering = ['-id']

    title = models.CharField(_('Title'), default='', null=False, blank=False, max_length=50)
    type = models.ForeignKey(Type, verbose_name=_('Type'), on_delete=models.SET_NULL,
                             default=None, null=True, blank=True)
    time = models.TimeField(_('Time'), default=datetime.time(hour=18, minute=00), null=False)
    date = models.DateField(_('Date'), default=tomorrow)
    trainer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                verbose_name=_('Trainer'), related_name='events_as_trainer')
    participants = models.ManyToManyField(User, verbose_name=_('Participants'), blank=True,
                                          related_name='events_as_participant')
    schema = models.ForeignKey(EventSchema, on_delete=models.SET_NULL, null=True, blank=True,
                               verbose_name=_('Schema'), related_name='events')

    participants_limit = models.IntegerField(_('Limit of participants'), default=10)
    register_time_limit = models.PositiveSmallIntegerField(_('Register time limit (minutes)'),
                                                           default=0, null=False, blank=False)
    unregister_time_limit = models.PositiveSmallIntegerField(_('Unregister time limit (minutes)'),
                                                             default=0, null=False, blank=False)

    def register_user(self, user, ticket=None):
        if user in self.participants.all():
            raise UserInParticipants(f'{user} is already registered in event {self}!')
        if self.register_time_passed():
            raise RegisterTimePassed(f'It\' too late to register to event {self}!')
        if self.participants.all().count() >= self.participants_limit:
            raise ParticipantsFull(f'Limit of participants ({self.participants_limit}) in event {self}!')

        if not ticket:
            ticket = user.get_ticket(self.type)

        if ticket:
            self.participants.add(user)
            ticket.usages_left -= 1
            ticket.save()
            EventRegistration.objects.create(
                event=self, user=user, ticket=ticket, direction=1,
                ticket_usages_left_after_register=ticket.usages_left
            )
        else:
            raise NoValidTicketFound(f'There is no valid ticket for user {user} and event {self}!')

    def unregister_user(self, user, ticket=None):
        if user not in self.participants.all():
            raise UserNotInParticipants(f'{user} is not registered in event {self}!')
        if self.unregister_time_passed():
            raise UnregisterTimePassed(f'It\' too late to unregister from event {self}!')

        if not ticket:
            ticket = user.get_ticket(self.type)

        if ticket:
            self.participants.remove(user)
            ticket.usages_left += 1
            ticket.save()
            EventRegistration.objects.create(
                event=self, user=user, ticket=ticket, direction=-1,
                ticket_usages_left_after_register=ticket.usages_left
            )
        else:
            raise NoValidTicketFound(f'There is no valid ticket for user {user} and event {self}! '
                                     f'Cannot resolve unregister.')

    def register_time_passed(self):
        return datetime.datetime.now() > datetime.datetime.combine(self.date, self.time) - datetime.timedelta(minutes=self.register_time_limit)

    def unregister_time_passed(self):
        return datetime.datetime.now() > datetime.datetime.combine(self.date, self.time) - datetime.timedelta(minutes=self.unregister_time_limit)

    def __str__(self):
        return f'{self.title} ({self.date.strftime("%d.%m.%Y")} | {self.time})'


class EventRegistration(TimestampedModel):
    class Meta:
        ordering = ['-id']

    DIRECTIONS = [
        (1, _('In')),
        (-1, _('Out')),
    ]

    user = models.ForeignKey(User, verbose_name=_('User'), on_delete=models.SET_NULL, null=True,
                             related_name='event_registrations')
    ticket = models.ForeignKey(Ticket, verbose_name=_('Ticket'), on_delete=models.SET_NULL, null=True)
    ticket_usages_left_after_register = models.SmallIntegerField(_('Ticket\'s usages left after registering'))
    event = models.ForeignKey(Event, verbose_name=_('Event'), on_delete=models.SET_NULL, null=True)
    direction = models.SmallIntegerField(_('Registering'), choices=DIRECTIONS, default=DIRECTIONS[0])
