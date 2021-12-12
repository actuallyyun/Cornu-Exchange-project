from django import forms
from .models import User, Listing, Bid, Comment, Watchlist
from django.forms.fields import ImageField


class NewListingForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    description = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control'}))
    category = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    starting_bid = forms.IntegerField(
        label="Starting Price:")
    listing_image = forms.ImageField(label="Add an image")


class BiddingForm(forms.Form):
    bid = forms.IntegerField(widget=forms.TextInput(
        attrs={'class': 'form-control'}), label="Your bid:")

    def __init__(self, data, listing):
        self.listing = listing
        super().__init__(data)

    def clean_bid(self):
        bidding_price = self.cleaned_data['bid']
        # Get the starting price of the listing
        starting_bid = self.listing.starting_bid
        # get the max existing bids
        max_bid = self.highest_bid()
        valid_bid_lower_bound = max_bid or starting_bid
        if bidding_price <= valid_bid_lower_bound:
            raise forms.ValidationError("Bid too low")
        return bidding_price


class AddCommentsForm(forms.Form):
    comments = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control'}), label="")
