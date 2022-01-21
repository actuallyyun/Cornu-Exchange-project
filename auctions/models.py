from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.core.exceptions import TooManyFieldsSent
from django.db import models
from django.db.models.base import Model
from django.db.models.fields import BooleanField, related
from django.utils import timezone
from django.db.models import Max


class User(AbstractUser):

    pass

    def watchlists(self):
        return [w for w in list(Watchlist.objects.filter(user=self))]

    def all_listings(self):
        return list(Listing.objects.filter(user=self))

    def active_listings(self):
        return [l for l in list(self.all_listings()) if l.active == True]

    def closed_listings(self):
        return [l for l in list(self.all_listings()) if l.active == False]

    def biddings(self):
        return list(Bid.objects.filter(user=self))


class Listing(models.Model):
    starting_bid = models.PositiveIntegerField(default=0)
    title = models.CharField(max_length=64, default="title")
    description = models.TextField(
        default="textcontent", blank=True, null=True)
    photo = models.ImageField(null=True, blank=True,
                              upload_to="images/", default="images/default.jpeg",)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="listing", null=True)
    active = BooleanField(default=True)
    price_sold_for = models.IntegerField(default=0, blank=True)
    date_listed = models.DateField(default=timezone.now)
    category = models.CharField(max_length=64, null=True, blank=True)

    def highest_bid(self):
        if [b.offer for b in list(Bid.objects.filter(item=self))]:
            return max([b.offer for b in list(Bid.objects.filter(item=self))])
        else:
            return 0

    def comments(self):
        return list(Comment.objects.filter(listing=self))

    def categories(self):
        return [c for c in list(Listing.objects.values_list('category', flat=True)) if c != None]


class Bid(models.Model):
    item = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="bids", null=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="bids", null=True)
    offer = models.PositiveIntegerField(null=True)
    date_created = models.DateTimeField(
        default=timezone.now, null=True)


class Comment(models.Model):
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True)
    content = models.TextField()
    date_commented = models.DateTimeField(
        default=timezone.now, null=True)


class Watchlist(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True)
    item = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="lists", null=True)
