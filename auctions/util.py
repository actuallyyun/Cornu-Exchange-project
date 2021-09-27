from auctions.views import category
from .models import User, Listing, Bid, Comment, Watchlist


def list_categories():
    # Returns a list of all names of listing categories
    categories = Listing.objects.values_list(
        'category', flat=True).order_by("category")
    return categories
