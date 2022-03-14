from django.db import models
from django.utils.translation import gettext_lazy as _

from manager.models import TimestampModel
from users.models import User


class Payment(TimestampModel):
    amount = models.DecimalField(_('Amount'), max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, verbose_name=_('User'), on_delete=models.SET_NULL,
                             related_name='payments', null=True, blank=True)
