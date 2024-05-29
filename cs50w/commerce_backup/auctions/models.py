from django.db import models

from user.models import User


class Categories(models.Model):
    name = models.CharField(max_length=100)
    

class Listings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    starting_bid = models.FloatField()
    image_url = models.URLField(blank=True, null=True)
    categories = models.ManyToManyField(Categories, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)


class Bids(models.Model):
    listings = models.ForeignKey(Listings, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bid = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    listings = models.ForeignKey(Listings, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(max_length=150)
    timestamp = models.DateTimeField(auto_now_add=True)



