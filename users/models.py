from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    first_name = models.CharField(_("first name"), max_length=32)
    last_name = models.CharField(_("last name"), max_length=32)
    email = models.EmailField(_("email address"), blank=True, unique=True)

    trainer = models.BooleanField(_('trainer'), default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.get_full_name()
