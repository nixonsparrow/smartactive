from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    first_name = models.CharField(_("First name"), max_length=32)
    last_name = models.CharField(_("Last name"), max_length=32)
    email = models.EmailField(_("Email address"), blank=True, unique=True)

    trainer = models.BooleanField(_('Trainer'), default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.get_full_name()

    def get_ticket(self, event_type):
        return self.tickets.filter(event_type=event_type, usages_left__gt=0).first()

    def register_on_event_with_ticket(self, event):
        ticket = self.get_ticket(event_type=event.type)
        if ticket:
            event.register_user(self)
