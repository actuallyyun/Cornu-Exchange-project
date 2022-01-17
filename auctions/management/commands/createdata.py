import email
from django.core.management.base import BaseCommand
from faker import Faker
import faker.providers
from auctions.models import User, Listing, Bid, Comment, Watchlist
import random

CATEGORIES = ["Electronics",
              "Collectibles & Art",
              "Fashion",
              "Motors",
              "Toys & Hobbies",
              "Sporting Goods",
              "Health & Beauty",
              "Books, Movies & Music",
              "Business & Industrial",
              "Home & Garden",
              "Others", ]

PRODUCTS = ["kimchi",
            "bread",
            "climbing pants",
            "climbing shoes",
            "pillow",
            "T-shirt",
            "spinach",
            "haircut",
            "speaker",
            "Boots",
            "shoes",
            "sweater", ]

USERS = list(User.objects.all())

LISTINGS = list(Listing.objects.all())


class Provider(faker.providers.BaseProvider):
    def auctions_category(self):
        return self.random_element(CATEGORIES)

    def auctions_product(self):
        return self.random_element(PRODUCTS)

    def auctions_user(self):
        return self.random_element(USERS)

    def auctions_item(self):
        return self.random_element(LISTINGS)


class Command(BaseCommand):
    help = "Command information"

    def handle(self, *args, **kwargs):

        fake = Faker(["nl_NL"])
        fake.add_provider(Provider)

        # Generate random users
        # for _ in range(10):
        #     User.objects.create(username=fake.first_name(), email=fake.ascii_email(
        #     ), password=fake.bothify(text='##???###??##????'))

        # Generate random listings

        # for _ in range(10):
        #     user = fake.auctions_user()
        #     starting_bid = random.randint(1, 999)
        #     title = fake.text(max_nb_chars=30)
        #     description = fake.paragraph(
        #         nb_sentences=6, variable_nb_sentences=True)
        #     Listing.objects.create(starting_bid=starting_bid,
        #                            user=user,
        #                            title=title,
        #                            description=description,
        #                            category=fake.unique.auctions_category())

        # for i in list(Listing.objects.all()):
        #     # i.photo = "images/20210527-baechu-kimchi-vicky-wasik-seriouseats-seriouseats-3-18a2d6d7d1d74a7a82c_4C1LTps.jpeg"
        #     i.category = fake.unique.auctions_category()
        #     i.save()

        # Delete all listings
        # for i in list(Listing.objects.all()):
        #     i.delete()

        # Generate bids
        # for _ in range(10):
        #     Bid.objects.create(item=fake.auctions_item(
        #     ), user=fake.auctions_user(), offer=random.randint(30, 990))

        # Generate comments
        # for _ in range(10):
        #     Comment.objects.create(listing=fake.auctions_item(
        #     ), user=fake.auctions_user(), content=fake.text(max_nb_chars=40))
