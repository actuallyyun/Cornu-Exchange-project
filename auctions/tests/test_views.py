from django.test import TestCase, testcases
from auctions.models import *
from django.http import request, response
from django.test.client import Client
from django.urls import reverse
from auctions.forms import *
from urllib.parse import urlencode


class TestUrls(TestCase):
    """ Test all urls are correct and functioning """

    def test_index_view_rendered_correctly(self):
        """ Setup test data """
        u1 = User.objects.create(username="a")
        u2 = User.objects.create(username="b")
        l1 = Listing.objects.create(user=u1, category="food", starting_bid=5)
        l2 = Listing.objects.create(user=u2, category="car")
        bid1 = Bid.objects.create(item=l1, user=u1, offer=6)
        bid2 = Bid.objects.create(item=l1, user=u2, offer=3)
        c1 = Comment.objects.create(listing=l1, user=u1, content="testcontent")
        c2 = Comment.objects.create(
            listing=l1, user=u2, content="testcontent2")
        w1 = Watchlist.objects.create(user=u1, item=l1)
        w2 = Watchlist.objects.create(user=u1, item=l2)

        c = Client()
        response = c.get("")
        """ It renders the correct template """
        self.assertTemplateUsed(
            response, 'auctions/index.html', 'auctions/layout.html')

    def test_home_view_rendered_correctly(self):
        """ Setup test data """
        u1 = User.objects.create(username="a")
        """ Force login u1 """
        self.client.force_login(u1)
        response = self.client.get("/1/home/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'auctions/home.html', 'auctions/layout.html')

    def test_listing_page_render_conrrectly(self):
        """ Setup test data """
        u1 = User.objects.create(username="a")
        u2 = User.objects.create(username="b")
        l1 = Listing.objects.create(
            user=u1, category="food", starting_bid=5)
        l2 = Listing.objects.create(user=u2, category="car")
        bid1 = Bid.objects.create(item=l1, user=u1, offer=6)
        bid2 = Bid.objects.create(item=l1, user=u2, offer=3)
        c1 = Comment.objects.create(
            listing=l1, user=u1, content="testcontent")
        c2 = Comment.objects.create(
            listing=l1, user=u2, content="testcontent2")
        w1 = Watchlist.objects.create(user=u1, item=l1)
        w2 = Watchlist.objects.create(user=u1, item=l2)

        """ Force login u1 """
        c = Client()
        c.force_login(u1)
        """ If request method is GET, returns the listing page """
        response = c.get('/listings/1/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'auctions/listing.html', 'auctions/layout.html')

        """ If the request method is POST, render the bidding form """
        response = c.post('/listings/1/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('biddingform', response.context)

    def test_category_page_render_correctly(self):
        """ Setup test data """
        u1 = User.objects.create(username="a")
        u2 = User.objects.create(username="b")
        l1 = Listing.objects.create(
            user=u1, category="food", starting_bid=5)
        l2 = Listing.objects.create(user=u2, category="car")
        bid1 = Bid.objects.create(item=l1, user=u1, offer=6)
        bid2 = Bid.objects.create(item=l1, user=u2, offer=3)
        c1 = Comment.objects.create(
            listing=l1, user=u1, content="testcontent")
        c2 = Comment.objects.create(
            listing=l1, user=u2, content="testcontent2")
        w1 = Watchlist.objects.create(user=u1, item=l1)
        w2 = Watchlist.objects.create(user=u1, item=l2)

        """ It returns the correct category requested """
        response = Client().get('/category/car/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual('car', response.context['category'])
        self.assertEqual(l2, response.context['listings'][0])


class TestCreateListingFunction(TestCase):
    """ Test listing forms are functioning, and all the data are handled corrcty """

    def test_get(self):
        """ Setup test data """
        c = Client()
        u1 = User.objects.create(username="a")
        c.force_login(u1)

        """ When the request mothod is GET, it shows the listing form """
        response = c.get('/new/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('new_listing_form', response.context)

    def test_post_fail(self):
        """ Setup test data """
        c = Client()
        u1 = User.objects.create(username="a")
        c.force_login(u1)

        """ When the request method is POST, but the form is not valid, it raises a 404 error """
        response = c.post('/new/')
        self.assertEqual(response.status_code, 404)

    # def test_post_sucess(self):
    #     """ Setup test data """
    #     u1 = User.objects.create(username='a')
    #     l1 = Listing.objects.create()
    #     self.client.force_login(u1)

    #     """ When the request mothod is POST, it creats a new listing instance """
    #     data = urlencode({'title': 'testtitle',
    #                       'description': 'testdescription',
    #                       'starting_bid': 5,
    #                       'category': 'home',
    #                       'listing_image': ''
    #                       })
    #     response = self.client.post(
    #         '/new/', data, content_type="application/x-www-form-urlencoded")
    #     print(response)
    #     """ It redirects the user to the newly created listing page """
    #     self.assertEqual(response.status_code, 302)

    #     """ Data is saved correctly in the database """
    #     self.assertTrue(Listing.objects.filter(title='testtitle').exists())


class TestAddCommentsFunction(TestCase):
    def test_get(self):
        """ Setup test data """
        u1 = User.objects.create(username='a')
        l1 = Listing.objects.create()
        self.client.force_login(u1)

        """ When the request mothod is GET, it shows the listing form """
        response = self.client.get('/comment/1/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('addcommentsform', response.context)

    def test_post_sucess(self):
        """ Setup test data """
        u1 = User.objects.create(username='a')
        l1 = Listing.objects.create()
        self.client.force_login(u1)

        """ When the request mothod is POST, it shows the listing form """
        data = urlencode({'comments': 'testcomment'})
        response = self.client.post(
            '/comment/1/', data, content_type="application/x-www-form-urlencoded")
        self.assertEqual(response.status_code, 302)
        """ Assert the comment instance exists in the database """
        self.assertTrue(Comment.objects.filter(content='testcomment').exists())

    def test_post_fail(self):
        """ Setup test data """
        u1 = User.objects.create(username='a')
        l1 = Listing.objects.create()
        self.client.force_login(u1)

        """ When the request mothod is POST but the form is invalid, it raises 404 """
        response = self.client.post(
            '/comment/1/')
        self.assertEqual(response.status_code, 404)


class TestWatchlistView(TestCase):
    def test_get_add_watchlist_sucess(self):
        """ When the request method is GET, it adds an item to the watchlist """
        """ Setup test data """
        u1 = User.objects.create(username='a')
        l1 = Listing.objects.create()
        self.client.force_login(u1)

        response = self.client.get('/watchlist/1/')
        """ User is redirected to the homepage """
        self.assertEqual(response.url, '/1/home/')
        """ Watchlist item is created in the database """
        self.assertTrue(Watchlist.objects.filter(item=l1).exists())

    def test_get_add_watchlist_fail(self):
        """ Setup test data """
        u1 = User.objects.create(username='a')
        l1 = Listing.objects.create()
        w1 = Watchlist.objects.create(user=u1, item=l1)
        self.client.force_login(u1)
        response = self.client.get('/watchlist/1/')
        """ User is redirected to the listing page """
        self.assertEqual(response.url, '/listings/1/')

    def test_post_delete_sucess(self):
        """ Setup test data """
        u1 = User.objects.create(username='a')
        l1 = Listing.objects.create()
        w1 = Watchlist.objects.create(user=u1, item=l1)
        self.client.force_login(u1)

        response = self.client.post('/watchlist/1/')
        """ User is redirected to the homepage """
        self.assertEqual(response.url, '/1/home/')
        """ Watchlist item is deleted in the database """
        self.assertFalse(Watchlist.objects.filter(item=l1).exists())


class TestCloseListingView(TestCase):
    def test_close_listing_sucess(self):
        """ Setup test data """
        u1 = User.objects.create(username='a')
        l1 = Listing.objects.create(user=u1)
        self.client.force_login(u1)

        response = self.client.get('/close/1/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context['message'], "Close listing successful!")
        # TODO status is changed successfully in the database
