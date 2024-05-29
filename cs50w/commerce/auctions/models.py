from django.db import models

from django.contrib.auth.models import AbstractUser

class Category(models.Model):
    name = models.CharField(max_length=100)

class User(AbstractUser):
    watchlist = models.ManyToManyField('Listings', related_name='watchlist')

class Listings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    starting_bid = models.FloatField()
    image_url = models.URLField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    is_closed = models.BooleanField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

class Bids(models.Model):
    listings = models.ManyToManyField(Listings, related_name='bids')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bid = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    listings = models.ManyToManyField(Listings, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(max_length=150)
    timestamp = models.DateTimeField(auto_now_add=True)
