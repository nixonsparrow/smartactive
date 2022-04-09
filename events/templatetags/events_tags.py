from django import template

register = template.Library()


@register.filter(name='has_ticket')
def has_ticket(user, event):
    return user.get_ticket(event.type)


@register.filter(name='can_register')
def can_register(user, event):
    return user.can_register(event)
