from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.core.exceptions import TooManyFieldsSent
from django.db import models
from django.db.models.base import Model
from django.db.models.fields import BooleanField, related
from django.utils import timezone


class User(AbstractUser):

    pass


class Listing(models.Model):
    starting_bid = models.PositiveIntegerField()
    title = models.CharField(max_length=64)
    description = models.TextField(default="textcontent")
    photo = models.ImageField(null=True, blank=True,
                              upload_to="images/", default=0)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, default=1, related_name="listing")
    active = BooleanField(default=True)
    price_sold_for = models.IntegerField(default=0, blank=True)
    date_listed = models.DateField(default=timezone.now)
    category = models.CharField(
        max_length=10,
        default='HOME'
    )

    def __str__(self):
        return f'{self.title}'


class Bid(models.Model):
    item = models.ForeignKey(
        Listing, on_delete=models.CASCADE, default=1, related_name="bids")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, default=1, related_name="bids")
    offer = models.IntegerField(default=0)
    date_created = models.DateTimeField(
        default=timezone.now)


class Comment(models.Model):
    listing = models.ForeignKey(
        Listing, default=1, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(
        User, default=1, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    date_commented = models.DateTimeField(
        default=timezone.now)


class Watchlist(models.Model):
    user = models.ForeignKey(
        User, default=1, on_delete=models.CASCADE, related_name="watchlists")
    item = models.ForeignKey(
        Listing, default=1, on_delete=models.CASCADE, related_name="watchlists")

    def __str__(self):
        return f"{self.user} ({self.item})"
