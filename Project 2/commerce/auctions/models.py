from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Bids(models.Model):
    user = models.CharField(max_length=64)
    title = models.CharField(max_length=64)
    listingid = models.IntegerField(primary_key=True)
    bid = models.IntegerField()

class Listing(models.Model):
    seller = models.CharField(max_length=64)
    title = models.CharField(max_length=64)
    description = models.TextField()
    starting_bid = models.IntegerField()
    category = models.CharField(max_length=64)
    image_link = models.CharField(
        max_length=200, default=None, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


