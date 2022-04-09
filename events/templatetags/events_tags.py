from django import template
from django.contrib.auth.models import AnonymousUser

register = template.Library()


@register.filter(name='has_ticket')
def has_ticket(user, event):
    if isinstance(user, AnonymousUser):
        return False
    return user.get_ticket(event.type)


@register.filter(name='can_register')
def can_register(user, event):
    if isinstance(user, AnonymousUser):
        return False
    return user.can_register(event)
