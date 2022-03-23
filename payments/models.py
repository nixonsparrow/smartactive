from django.db import models
from django.utils.translation import gettext_lazy as _

from events.models import Type
from manager.models import TimestampedModel
from users.models import User


class Ticket(TimestampedModel):
    class Meta:
        verbose_name = _('Ticket')
        verbose_name_plural = _('Tickets')

    user = models.ForeignKey(User, verbose_name=_('User'), on_delete=models.SET_NULL, null=True, blank=True)
    active = models.BooleanField(verbose_name=_('Active'), default=True)

    event_type = models.ForeignKey(Type, default=None, on_delete=models.SET_NULL,
                                   related_name='tickets', null=True, blank=False)
    usages_left = models.PositiveSmallIntegerField(verbose_name=_('Usages left'), default=1, null=False, blank=False)

    def __str__(self):
        return f'{_("Ticket")} ({self.id}): {self.user if self.user else _("Incognito")}'


class Payment(TimestampedModel):
    class Meta:
        verbose_name = _('Payment')
        verbose_name_plural = _('Payments')

    amount = models.DecimalField(_('Amount'), max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='payments', null=True, blank=True)
    initial_entries = models.PositiveSmallIntegerField(_('Initial entries'), default=1, null=False, blank=False)

    ticket = models.OneToOneField(Ticket, on_delete=models.SET_NULL, default=None, null=True, blank=True)

    def __str__(self):
        return f'{_("Payment")} ({self.id}): {self.user if self.user else _("Incognito")}'
