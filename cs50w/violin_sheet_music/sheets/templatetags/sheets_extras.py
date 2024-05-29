from django import template
from django.template.defaultfilters import stringfilter

import locale

register = template.Library()
locale.setlocale(locale.LC_ALL, "en_US.UTF-8")


@register.filter()
def capitalize(str):
    return str.capitalize()


@register.filter()
def range_custom(num):
    return range(1, int(num))
