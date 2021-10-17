
from .models import User, Listing, Bid, Comment, Watchlist
from django.db.models import Max


def list_categories():
    # Returns a list of all names of listing categories
    categories = Listing.objects.values_list(
        'category', flat=True).distinct().order_by("category")
    return categories


def max_bid(listing):
    # Returns the max bidding price by its id. If no bids, returns None
    return listing.bids.all().aggregate(Max('offer')).get('offer__max')
