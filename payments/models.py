from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from events.models import Ticket, Type
from manager.models import TimestampedModel


class Payment(TimestampedModel):
    class Meta:
        verbose_name = _('Payment')
        verbose_name_plural = _('Payments')
        ordering = ['-id']

    amount = models.DecimalField(_('Amount'), max_digits=10, decimal_places=2)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('User'), on_delete=models.SET_NULL,
                             related_name='payments', null=True, blank=True)
    initial_usages = models.PositiveSmallIntegerField(_('Initial usages'), default=1, null=False, blank=False)

    event_type = models.ForeignKey(Type, verbose_name=_('Type'), default=None, on_delete=models.SET_NULL,
                                   related_name='payments', null=True, blank=True)
    ticket = models.OneToOneField(Ticket, verbose_name=_('Ticket'), on_delete=models.SET_NULL, default=None, null=True, blank=True)

    def __str__(self):
        return f'{_("Payment")} ({self.id}): {self.user if self.user else _("Incognito")}'
