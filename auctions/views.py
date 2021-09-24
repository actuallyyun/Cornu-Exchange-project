from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.http.request import RAISE_ERROR
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, Listing, Bid, Comment, Watchlist
from django import forms


class NewListingForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput)
    description = forms.CharField(widget=forms.Textarea)
    starting_bid = forms.IntegerField(label="Starting Price:")


class BiddingForm(forms.Form):
    bid = forms.IntegerField(label="Your bid:")


def index(request):
    listings = Listing.objects.all()

    return render(request, "auctions/index.html", {
        "listings": listings
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

        # get the user
        seller = request.user

        # get the listing data from the forms
        title = request.POST['title']
        description = request.POST['description']
        starting_bid = request.POST['starting_bid']
        listing = Listing(title=title, description=description,
                          starting_bid=starting_bid, user=seller)
        # TODO validate the data & error checking
        listing.save()
        return HttpResponseRedirect(reverse('index'))

    else:
        return render(request, "auctions/newlisting.html", {
            "new_listing_form": NewListingForm()
        })


@login_required
def home(request, id):
    return render(request, "auctions/home.html", {
        'user_id': id
    })


def listing(request, title):

    if request.method == "POST":
        return Http404

    else:
        try:
            listing = Listing.objects.get(title=title)
        except Listing.DoesNotExist:
            raise Http404("Listing Not Found")

        return render(request, "auctions/listing.html", {
            "title": title,
            "listing": listing,
            "biddingform": BiddingForm()
        })


@login_required
def bid(request, title):

    bidder = request.user

    if request.method == "POST":
        form = BiddingForm(request.POST)
        if form.is_valid():

            bidding_price = form.cleaned_data['bid']
            # Get the starting price of the listing
            listing = Listing.objects.get(title=title)

            if bidding_price >= listing.starting_bid:
                # get the existing bids
                bids = Listing.objects.values_list(
                    'bids', flat=True).filter(title=title)

                for bid in bids:

                    # if there's no bit yet,directly save the new bit
                    if bid is not None:
                        if bidding_price < bid:
                            RAISE_ERROR("Bid failed.")

                bid = Bid(item=listing, user=bidder,
                          offer=bidding_price)
                bid.save()
                # redirect user to the home page
                id = bidder.id
                return HttpResponseRedirect(reverse('home', args=[id]))

            # display error messages if bid failed
            return render(request, "auctions/listing.html", {
                "errormessage": "Cannot bid lower than the listing price nor exisiting bids.",
                "biddingform": BiddingForm(),
                "title": title
            })

    return render(request, "auctions/listing.html", {
        "biddingform": BiddingForm()
    })

# User can add a listing to her wishlist


@login_required
def add_watchlist(request, title):
    listing = Listing.objects.get(title=title)
    user = request.user
    existing_watchlist = User.objects.values_list(
        'watchlists', flat=True).filter(username=user)
    if listing in existing_watchlist:
        # TODO return an error msg saying it already exists. Show remove button
        return HttpResponseRedirect(reverse('listing'), args=[title])
    new_watchlist = Watchlist(user=user, item=listing)
    new_watchlist.save()
    id = user.id
    return HttpResponseRedirect(reverse('home', args=[id]))


def close_listing(request, title):
    # Change the status of the listing to False
    # Find out the highest bidding, and show it to the user
    # Redirect to homepage
    return None
