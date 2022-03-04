from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    trainer = models.BooleanField('Trener', default=False)
