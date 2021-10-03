
from .models import User, Listing, Bid, Comment, Watchlist
from django.db.models import Max


def list_categories():
    # Returns a list of all names of listing categories
    categories = Listing.objects.values_list(
        'category', flat=True).distinct().order_by("category")
    return categories


def get_watchlist(user):
    # Returns a list of all watchlist that user added.If no such listing, returns None
    if user.watchlists.all().exists():
        return user.watchlists.all()
    else:
        return None


def get_user_listings(user):
    # Return a list of listing objects of this user
    if user.listing.all().exists():
        return user.listing.all()

    return None


def max_bid(listing):
    # Returns the max bidding price by its id. If no bids, returns None
    if listing.bids.all().exists():
        return listing.bids.all().aggregate(Max('offer')).get('offer__max')

    return None


def save_bid(listing, user, price):

    bid = Bid(item=listing, user=user,
              offer=price)
    bid.save()
