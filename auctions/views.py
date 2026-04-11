from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .forms import ListingForm, WatchListForm, BidsForm
from .models import User, Listing, WatchList, Bids


def index(request):
    return render(request, "auctions/index.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

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

        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

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


@login_required
def create_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.owner = request.user
            listing.save()
            return redirect("index")
    else:
        form = ListingForm()

    return render(request, "auctions/create_listing.html", {
        "form": form
    })


def listing(request, id=None):
    if id:
        listing = get_object_or_404(Listing, pk=id)
        return render(request, "auctions/listing.html", {
            "listing": listing
        })
    else:
        listings = Listing.objects.filter(active=True)
        return render(request, "auctions/listing.html", {
            "listings": listings
        })


@login_required
def watchlist_view(request, id):
    listing = get_object_or_404(Listing, pk=id)

    if request.method == "POST" and "watch_form" in request.POST:
        existing = WatchList.objects.filter(
            owner=request.user, listing=listing
        ).first()

        if existing:
            existing.delete()
        else:
            WatchList.objects.create(owner=request.user, listing=listing)

    return redirect("listing", id=id)

@login_required
def watchlist_page(request):
    watchlist = WatchList.objects.filter(owner=request.user)
    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist
    })


from django.contrib import messages

@login_required
def bidding(request, id):
    listing = get_object_or_404(Listing, pk=id)

    if request.method == "POST" and "bid_form" in request.POST:
        form = BidsForm(request.POST)

        if form.is_valid():
            bid = form.save(commit=False)
            bid.user = request.user
            bid.listing = listing

            # Get minimum required bid
            highest_bid = Bids.objects.filter(
                listing=listing
            ).order_by("-amount").first()

            min_bid = highest_bid.amount if highest_bid else listing.starting_price

            # Validate bid (>= allows matching starting price)
            if bid.amount >= min_bid:
                bid.save()
                listing.current_price = bid.amount
                listing.save()
                messages.success(request, f"Bid of ${bid.amount} placed successfully!")
            else:
                messages.error(
                    request, 
                    f"Bid must be at least ${min_bid}. You entered ${bid.amount}."
                )
        else:
            # Show form validation errors
            messages.error(request, f"Invalid bid: {form.errors}")

    return redirect("listing", id=id)
 
@login_required
def close_auction(request, id):
    listing = get_object_or_404(Listing, id=id)

    # Optional: only owner can close
    if request.user != listing.owner:
        return redirect("listing", id=id)

    listing.is_active = False
    listing.save()

    return redirect("listing", id=id)
