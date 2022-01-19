from functools import total_ordering
import os
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.checks import messages
from django.db import IntegrityError
from django.forms.fields import ImageField
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.http.request import RAISE_ERROR
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from . import forms
from .models import Bid, Comment, Listing, User, Watchlist


def index(request):
    try:
        listings = list(Listing.objects.all().filter(active=True))
    except:
        raise Http404('db not working')

    p = Paginator(listings, 5)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)

    try:
        listings = p.page(page_number)
    except PageNotAnInteger:
        listings = p.page(1)
    except EmptyPage:
        listings = p.page(p.num_pages)

    if len(listings) == 0:
        categories = ['No listings yet']
    else:
        categories = listings[0].categories()
    return render(request, "auctions/index.html", {
        "listings": listings,
        "categories": categories,
        'page_obj': page_obj
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
            messages.success(request, 'Login successful.')
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


# The user creates a listing by filing up the form
@login_required
def create_listing(request):
    # If the request method is "POST", create the lsiting
    if request.method == "POST":
        form = forms.NewListingForm(request.POST, request.FILES)
        if form.is_valid():
            seller = request.user
            # get the listing data from the forms
            title = request.POST['title']
            description = request.POST['description']
            starting_bid = request.POST['starting_bid']
            category = request.POST['category']
            img = request.FILES['listing_image']
            listing = Listing(title=title, description=description,
                              starting_bid=starting_bid, user=seller, category=category, photo=img)

            listing.save()

            # Redirect user to the new listing page
            return HttpResponseRedirect(reverse('listing', args=[listing.id]))
        else:
            raise Http404
    # If not, render the create listing page with the form
    else:
        return render(request, "auctions/newlisting.html", {
            "new_listing_form": forms.NewListingForm(),
        })


# The user's home page. It displays her listings, watchlists and bids.
@login_required
def home(request, user_id):
    user = request.user
    if user.closed_listings():
        total_earnings = sum(
            [l.price_sold_for for l in user.closed_listings()])
    else:
        total_earnings = 0

    return render(request, "auctions/home.html", {
        'listings': user.active_listings(),
        'sold': user.closed_listings(),
        'watchlist': user.watchlists(),
        "bids": user.biddings(),
        "total_earnings": total_earnings
    })


def listing(request, listing_id):
    # If request method is POST, place a bid
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        form = forms.BiddingForm(request.POST, listing)
        bidder = request.user

        if form.is_valid():
            bidding_price = form.cleaned_data['bid']
            bid = Bid(item=listing, user=bidder,
                      offer=bidding_price)
            bid.save()
            messages.success(request, "Bidding successful!")
            return HttpResponseRedirect(reverse('home', args=[bidder.id]))

        # display error messages if bid failed
        return render(request, "auctions/listing.html", {
            "biddingform": form,
            "listing": listing,
            "categories": listing.categories()
        })

    else:
        # If request method is GET, show the listing page
        listing = Listing.objects.get(id=listing_id)

        current_bid = listing.highest_bid() or listing.starting_bid

        return render(request, "auctions/listing.html", {
            "listing": listing,
            "biddingform": forms.BiddingForm(None, listing),
            "addcommentsform": forms.AddCommentsForm(),
            "categories": listing.categories(),
            "comments": listing.comments(),
            "current_bid": current_bid
        })


# User can add and remove a listing to her wishlist
@login_required
def watchlist(request, listing_id):
    user = request.user

    # If the request is sent by the <a> tag through "GET" method, attemp to add an item to the watchlist
    if request.method == "GET":
        listing = Listing.objects.get(pk=listing_id)

        # If item already in the watchlist, display an error msg and send user back to the listing page
        if listing in [w.item for w in user.watchlists()]:
            messages.error(
                request, "Lisitng already exists in your watchlist.")
            return HttpResponseRedirect(reverse('listing', args=[listing_id]))

        # Else, add the item to the watchlist
        else:
            new_watchlist = Watchlist(user=user, item=listing)
            new_watchlist.save()

            # Redirect user to the home page
            return HttpResponseRedirect(reverse('home', args=[user.id]))

    # If the request is sent by the form through "POST" method, remove the item by deleting the watclist object
    else:
        # Get the watchlist instance with its id
        watchlist = get_object_or_404(Watchlist, id=listing_id)

        watchlist.delete()
        messages.success(request, "Item removed successful.")

        # redirect user to her homepage
        return HttpResponseRedirect(reverse('home', args=[user.id]))


@login_required
def close_listing(request, listing_id):
    if request.method == "GET":
        listing = Listing.objects.get(pk=listing_id)
        # Change the status of the listing to False
        listing.active = False
        listing.save()
        # Redirect to listing page
        return render(request, 'auctions/close.html', {
            "message": "Close listing successful!",
            "highest_bid": listing.highest_bid(),
            "listing": listing
        })
    else:
        return HttpResponseRedirect(reverse('listing', args=[listing_id]))


@login_required
def add_comments(request, listing_id):

    listing = Listing.objects.get(pk=listing_id)
    if request.method == "POST":
        form = forms.AddCommentsForm(request.POST)
        if form.is_valid():
            comments = form.cleaned_data['comments']
            # save the comment to the database
            comment = Comment(listing=listing,
                              user=request.user, content=comments)
            comment.save()
            return HttpResponseRedirect(reverse('listing', args=[listing_id]))
        else:
            raise Http404

    return render(request, 'auctions/listing.html', {
        "addcommentsform": forms.AddCommentsForm(),
        'listing': listing
    })


def category(request, category):
    # Retrive lisitngs from the category
    listings = Listing.objects.filter(category=category)
    return render(request, 'auctions/category.html', {
        'listings': listings,
        'category': category
    })
