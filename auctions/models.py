from django.contrib.auth.models import AbstractUser
from django.core.exceptions import TooManyFieldsSent
from django.db import models
from django.db.models.base import Model
from django.db.models.fields import BooleanField, related


class User(AbstractUser):

    pass


class Listing(models.Model):
    starting_bid = models.IntegerField()
    title = models.CharField(max_length=64)
    description = models.TextField(default="textcontent")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, default=1, related_name="seller")
    status = BooleanField(default=True)

    # class Category(models.TextChoices):
    #     Home = 'Home'
    #     Fashion = 'Fashion'

    def __str__(self):
        return f"{self.title} ({self.starting_bid}euros)"


class Bid(models.Model):
    item = models.ForeignKey(
        Listing, on_delete=models.CASCADE, default=1, related_name="bids")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, default=1, related_name="bids")
    offer = models.IntegerField(default=0)


class Comment(models.Model):
    listing = models.ForeignKey(Listing, default=1, on_delete=models.CASCADE)
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    content = models.TextField()


class Watchlist(models.Model):
    user = models.ForeignKey(
        User, default=1, on_delete=models.CASCADE, related_name="watchlists")
    item = models.ForeignKey(
        Listing, default=1, on_delete=models.CASCADE, related_name="watchlists")

    def __str__(self):
        return f"{self.user} ({self.item})"
