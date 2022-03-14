from django.db import models
from django.utils.translation import gettext_lazy as _

from manager.models import TimestampModel


class Payment(models.Model, TimestampModel):
    amount = models.DecimalField(_('Amount'), max_digits=10, decimal_places=2)
