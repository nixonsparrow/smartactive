from django import template
from wagtail.images.models import Image

from ..models import Menu

register = template.Library()


@register.simple_tag()
def get_menu(slug):
    try:
        return Menu.objects.get(slug=slug)
    except Menu.DoesNotExist:
        return None


@register.simple_tag()
def get_menu_logo(title):
    try:
        return Image.objects.filter(title=title).last()
    except Image.DoesNotExist:
        return None
