from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):

        user = self.model(email=email, is_superuser=False)

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None):

        user = self.model(email=email, is_superuser=True)

        user.set_password(password)
        user.save()
        return user


class User(AbstractUser):
    first_name = models.CharField(_("First name"), max_length=32)
    last_name = models.CharField(_("Last name"), max_length=32)
    email = models.EmailField(_("Email address"), blank=True, unique=True)

    trainer = models.BooleanField(_('Trainer'), default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.get_full_name()

    # TODO make more complex checking here
    def can_register(self, event):
        if self in event.participants.all():
            return False
        elif event.register_time_passed():
            return False
        elif event.is_full():
            return False
        elif not self.get_ticket(event.type):
            return False

        else:
            return True

    def get_ticket(self, event_type):
        return self.tickets.filter(event_type=event_type, usages_left__gt=0).first()

    def get_empty_ticket(self, event_type):
        return self.tickets.filter(event_type=event_type, usages_left=0).first()

    def register_on_event_with_ticket(self, event):
        ticket = self.get_ticket(event_type=event.type)
        if ticket:
            event.register_user(self)

    def register_on_event(self, event):
        self.register_on_event_with_ticket(event)

    def unregister_from_event(self, event):
        event.unregister_user(user=self)
