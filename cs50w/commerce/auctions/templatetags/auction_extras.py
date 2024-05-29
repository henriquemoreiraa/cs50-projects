from django import template
from django.template.defaultfilters import stringfilter

import locale

from auctions.models import User

register = template.Library()
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8') 


@register.filter()
def watchlist_len(user_pk): 
    user_watchlist = User.objects.get(pk=user_pk).watchlist.all()

    return len(user_watchlist)


@register.filter()
def format_currency(value): 
    return locale.currency(value, grouping=True, symbol=True)