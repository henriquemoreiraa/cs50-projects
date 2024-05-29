from django.contrib import admin

from auctions.models import Bids, Category, Listings, User ,Comment

# Register your models here.
admin.site.register(Listings)
admin.site.register(User)
admin.site.register(Bids)
admin.site.register(Comment)
admin.site.register(Category)