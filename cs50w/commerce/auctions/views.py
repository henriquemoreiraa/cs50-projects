from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import  HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render

from auctions.forms import ListingForm
from .models import Bids, Category, Listings, User, Comment

def index(request):
    category = request.GET.get('category', None)

    if category:
        auctions_listings = Listings.objects.filter(category=category)
    else: 
        auctions_listings = Listings.objects.all()

    return render(request, "auctions/index.html", {
        "auctions_listings": auctions_listings,
    })

def listings(request, id):
    listings = Listings.objects.get(pk=id)
     
    try:
        user_watchlist = User.objects.get(pk=request.user.pk).watchlist.get(pk=id)
    except:
        user_watchlist = None

    return render(request, "auctions/listings.html", {
        "listings": listings,
        "watchlist": user_watchlist,
        "num_bids": len(listings.bids.all()),
        "last_bid": listings.bids.last(),
        "message": request.GET.get('message', ''),
        "comments": Comment.objects.all()
    })


def close_listing(request, id):
    listing = Listings.objects.get(pk=id)
    listing.is_closed = True
    listing.save()

    return HttpResponseRedirect(reverse("listings", args=[id]))


def create_listing(request):
    if request.method == 'POST':
        data = request.POST
        form = ListingForm(data)

        if form.is_valid():
            user = User.objects.get(pk=request.user.pk)
            if data['category'] == 1:
                category = None
            else:
                category = Category.objects.get(pk=data['category'])

            new_listing = Listings(user=user, title=data["title"], description=data['description'], starting_bid=data['starting_bid'], image_url=data['image_url'], category=category)
            new_listing.save()

            return HttpResponseRedirect(reverse("listings", args=[new_listing.pk])) 
        
        return render(request, "auctions/create-listing.html", {
            'form': form
        })

    return render(request, "auctions/create-listing.html", {
        'form': ListingForm
    })


def comment(request, listing_id):
    user = User.objects.get(pk=request.user.pk)

    new_comment = Comment(user=user, comment=request.POST['comment'])
    new_comment.save()
    new_comment.listings.add(listing_id)

    return HttpResponseRedirect(reverse("listings", args=[listing_id]))


def watchlist(request):
    user = User.objects.get(pk=request.user.pk)

    if request.method == 'POST':
        listings_pk = request.POST["listings_pk"]

        try:
            user.watchlist.get(pk=listings_pk)
            user.watchlist.remove(listings_pk)
        except:
            user.watchlist.add(listings_pk)

        return HttpResponseRedirect(reverse("listings", args=[listings_pk]))
    
    watchlist_listings = user.watchlist.all()

    return render(request, "auctions/watchlist.html", {
        "watchlist_listings": watchlist_listings
    })


def bid(request, listing_pk):
    listing = Listings.objects.get(pk=listing_pk)
    listing_url = reverse(viewname="listings", args=[listing_pk]) 

    bid = float(request.POST["bid"])

    if listing.starting_bid > bid:
        return HttpResponseRedirect(f"{listing_url}?message=Your bid must be greater or equal than the listing starting bid!")

    try:
        if listing.bids.last().bid >= bid:
            return HttpResponseRedirect(f"{listing_url}?message=Your bid must be greater than the previous bid!")
    except:
        pass

    user = User.objects.get(pk=request.user.pk)

    new_bid = Bids(user=user, bid=bid)
    new_bid.save()
    new_bid.listings.add(listing_pk)

    return HttpResponseRedirect(reverse("listings", args=[listing_pk]))


def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.exclude(pk=1)
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")