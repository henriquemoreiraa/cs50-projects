
from django.shortcuts import render

from watchlist.models import Watchlist

from .models import Listings

def index(request):
    auctions_listings = Listings.objects.all()

    return render(request, "auctions/index.html", {
        "auctions_listings": auctions_listings,
    })

def listings(request, id):
    listings = Listings.objects.get(pk=id)
     
    try:
        user_watchlist = Watchlist.objects.get(user=request.user.pk).listings.get(pk=id)
    except:
        user_watchlist = None


    return render(request, "auctions/listings.html", {
        "listings": listings,
        "watchlist": user_watchlist
    })


