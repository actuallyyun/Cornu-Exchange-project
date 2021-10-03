from functools import total_ordering
from django.contrib.auth import authenticate, login, logout
from django.core.checks import messages
from django.db import IntegrityError
from django.forms.fields import ImageField
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.http.request import RAISE_ERROR
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, Listing, Bid, Comment, Watchlist
from . import util, forms

categories = util.list_categories()


def index(request):
    listings = Listing.objects.all().filter(active=True)
    return render(request, "auctions/index.html", {
        "listings": listings,
        "categories": categories
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


@login_required
def create_listing(request):

    if request.method == "POST":
        form = forms.NewListingForm(request.POST, request.FILES)
        # get the user
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
        return HttpResponseRedirect(reverse('listing', args=[title]))

    else:

        return render(request, "auctions/newlisting.html", {
            "new_listing_form": forms.NewListingForm(),
            "categories": categories
        })


@login_required
def home(request, user_id):
    user = request.user
    # Request watchlist of the user
    watchlist = util.get_watchlist(user)

    # Request listings of this user
    listings = util.get_user_listings(user)

    # Request bids of this user
    bids = user.bids.all()
    total_earnings = 0
    # if the result is not None
    if listings:
        listings_active = []
        listings_ended = []
    # get the objects
        for listing in listings:
            if listing.active == False:
                listings_ended.append(listing)
                total_earnings = total_earnings + listing.price_sold_for
            else:
                listings_active.append(listing)
        return render(request, "auctions/home.html", {
            'listings': listings_active,
            'sold': listings_ended,
            "categories": categories,
            'watchlist': watchlist,
            "bids": bids,
            "total_earnings": total_earnings
        })

    return render(request, "auctions/home.html", {
        "categories": categories
    })


def listing(request, title):
    listing = Listing.objects.get(title=title)
    # Get the comments of this listing
    if listing.comments.all().exists():
        comments = listing.comments.all()
    else:
        comments = None

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "biddingform": forms.BiddingForm(),
        "addcommentsform": forms.AddCommentsForm(),
        "categories": categories,
        "comments": comments
    })


@login_required
def bid(request, title):

    if request.method == "POST":
        form = forms.BiddingForm(request.POST)
        listing = Listing.objects.get(title=title)
        bidder = request.user

        if form.is_valid():

            bidding_price = form.cleaned_data['bid']
            # Get the starting price of the listing
            starting_bid = listing.starting_bid
            # get the max existing bids

            max_bid = util.max_bid(listing)
            if max_bid and bidding_price > max_bid:

                util.save_bid(listing, bidder, bidding_price)
            elif not max_bid and bidding_price > starting_bid:

                util.save_bid(listing, bidder, bidding_price)
                # Tell user the bid succeded and redirect the user to her home page
                return HttpResponseRedirect(reverse('home', args=[bidder.id]))

            else:
                # display error messages if bid failed
                return render(request, "auctions/listing.html", {
                    "errormessage": "Cannot bid lower than the listing price nor exisiting bids.",
                    "biddingform": forms.BiddingForm(),
                    "listing": listing,
                    "categories": categories
                })

    return render(request, "auctions/listing.html", {
        "biddingform": forms.BiddingForm()
    })


# User can add a listing to her wishlist
@login_required
def add_watchlist(request, title):
    user = request.user

    if request.method == "POST":
        listing = Listing.objects.get(title=title)

        # Retrieve the existing watchlist
        if user.watchlists.all().filter(item=listing).exists():
            errormessagefromwatchlist = "This listing is already in your watchlist."
            return HttpResponseRedirect(reverse('listing', args=[title]))

        else:
            new_watchlist = Watchlist(user=user, item=listing)
            new_watchlist.save()
            # Redirect user to the watchlist page
            return render(request, 'auctions/watchlist.html', {
                "watchlist": user.watchlists.all(),
                "categories": categories
            })
    else:
        return render(request, 'auctions/watchlist.html', {
            "watchlist": user.watchlists.all(),
            "categories": categories
        })


@login_required
def close_listing(request, title):
    listing = Listing.objects.get(title=title)
    highest_bid = util.max_bid(listing)
    if highest_bid:
        listing.price_sold_for = highest_bid
    # Change the status of the listing to False
    listing.active = False
    listing.save()
    # Redirect to listing page
    return render(request, 'auctions/close.html', {
        "messages": "Close listing successful!",
        "highest_bid": highest_bid,
        "listing": listing
    })


@login_required
def add_comments(request, title):

    listing = Listing.objects.get(title=title)
    if request.method == "POST":
        form = forms.utilAddCommentsForm(request.POST)
        if form.is_valid():
            comments = form.cleaned_data['comments']
            # save the comment to the database
            comment = Comment(listing=listing,
                              user=request.user, content=comments)
            comment.save()
        return HttpResponseRedirect(reverse('listing', args=[title]))

    return render(request, 'listing.html', {
        "addcommentsform": forms.AddCommentsForm()
    })


def category(request, category):
    # Retrive lisitngs from the category
    listings = Listing.objects.filter(category=category)
    return render(request, 'auctions/category.html', {
        'listings': listings,
        'category': category,
        "categories": categories
    })


@ login_required
def remove_watchlist(request, title):
    user = request.user
    if request.method == "POST":
        item = Listing.objects.get(title=title)
        user.watchlists.all().remove(item)
        return HttpResponseRedirect(reverse('watchlist'), args=[title])
