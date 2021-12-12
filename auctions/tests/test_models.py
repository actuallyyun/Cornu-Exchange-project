from django.test import TestCase
from auctions.models import *


class UserListingsTest(TestCase):

    def test_user_related_values(self):
        """ Setup test data """
        u1 = User.objects.create(username="a")
        u2 = User.objects.create(username="b")
        l1 = Listing.objects.create(user=u1, category="food", starting_bid=5)
        l2 = Listing.objects.create(user=u1, category="car")
        l3 = Listing.objects.create(user=u1, active=False)
        bid1 = Bid.objects.create(item=l1, user=u1, offer=6)
        bid2 = Bid.objects.create(item=l1, user=u2, offer=3)
        c1 = Comment.objects.create(listing=l1, user=u1, content="testcontent")
        c2 = Comment.objects.create(
            listing=l1, user=u2, content="testcontent2")
        w1 = Watchlist.objects.create(user=u1, item=l1)
        w2 = Watchlist.objects.create(user=u1, item=l2)

        """ Returns the correct watchlist of this user """
        u1_watchlist = u1.watchlists()
        self.assertEqual(len(u1_watchlist), 2)
        self.assertEqual(u2.watchlists(), [])

        """ Returns the correct all listing of this user """
        u1_listing = u1.all_listings()
        self.assertEqual(u1_listing[0], l1)

        """ Returns the active listings of u1 """
        u1_active_listings = u1.active_listings()
        self.assertEqual(len(u1_active_listings), 2)

        """ Returns closed listings of u1 """
        u1_closed_listings = u1.closed_listings()
        self.assertEqual(u1_closed_listings[0], l3)

        """ Returns the correct biddings of this user """
        u1_bidding = u1.biddings()
        self.assertEqual(u1_bidding[0], bid1)

    def test_listing_related_values(self):
        """ Setup test data """
        u1 = User.objects.create(username="a")
        u2 = User.objects.create(username="b")
        l1 = Listing.objects.create(user=u1, category="food", starting_bid=5)
        l2 = Listing.objects.create(user=u2, category="car")
        bid1 = Bid.objects.create(item=l1, user=u1, offer=6)
        bid2 = Bid.objects.create(item=l1, user=u2, offer=7)
        c1 = Comment.objects.create(listing=l1, user=u1, content="testcontent")
        c2 = Comment.objects.create(
            listing=l1, user=u2, content="testcontent2")

        """ Returns the correct highest bid"""
        self.assertEqual(l1.highest_bid(), 7)

        """ Returns the correct comments """
        c = l1.comments()
        self.assertEqual(len(c), 2)
        self.assertEqual(c[0], c1)

        """ Returns the correct categories """
        c = l1.categories()
        self.assertEqual(len(c), 2)
        self.assertEqual(c, ['food', 'car'])
