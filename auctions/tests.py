from django.http import response
from django.test import TestCase, Client
from django.db.models import Max
from . import forms, util
from .models import Bid, Comment, Listing, User, Watchlist
from django.contrib.auth import get_user_model

# Create your tests here.


class UsersManagersTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(username='testuser',
                                        email="normal@user.com", password="123")
        self.assertEqual(user.email, "normal@user.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)


class ListingTestCase(TestCase):

    def setUp(self):

        # Create users.
        u1 = User.objects.create()

        # Create listings.
        l1 = Listing.objects.create(starting_bid=5, title="listing1",
                                    user=u1, description="listing1")
        l2 = Listing.objects.create(starting_bid=10, title="listing2",
                                    user=u1, description="listing2")

        # Create bids
        b1 = Bid.objects.create(item=l1, user=u1, offer=6)
        b2 = Bid.objects.create(item=l1, user=u1, offer=3)

    def test_index(self):
        """ Index page is correctly displayed. """
        c = Client()
        response = c.get("")
        print(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["listings"].count(), 2)

    def test_invalid_listing_page(self):
        """ Try to display invalid page should invoke 404. """
        max_id = Listing.objects.all().aggregate(Max("id"))["id__max"]
        c = Client()
        response = c.get(f"{max_id}")
        self.assertEqual(response.status_code, 404)
