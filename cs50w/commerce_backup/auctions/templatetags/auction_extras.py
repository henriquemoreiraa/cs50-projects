from django import template
from django.template.defaultfilters import stringfilter

import locale

from watchlist.models import Watchlist

register = template.Library()
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8') 


@register.filter()
def watchlist_len(user_pk): 
    try:
        user_watchlist = Watchlist.objects.get(user=user_pk).listings.all() 
    except:
        user_watchlist = []

    return len(user_watchlist)


@register.filter()
def format_currency(value): 
    return locale.currency(value, grouping=True, symbol=True)